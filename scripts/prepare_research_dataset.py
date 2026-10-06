from pathlib import Path
import numpy as np
import pandas as pd
from scipy.special import logit, expit
from scipy.stats import spearmanr
import json, math

ROOT = Path(__file__).resolve().parents[1]
PRED = ROOT/'predictions'
META = ROOT/'campus_real_metadata'
PRED.mkdir(exist_ok=True)
META.mkdir(exist_ok=True)
SEED=20260912

# ---------------- core manuscript constants ----------------
BUILDINGS=[f'B{i:02d}' for i in range(1,24)]
TYPES=(['Lecture Hall']*8+['Research Lab']*7+['Administrative Office']*5+['Sports Facility']*3)
AREAS=[11000,10500,12000,9500,11500,10500,10500,13500,
       12500,13000,12000,15000,13000,12500,13000,
       10000,9500,11000,10500,11000,
       17000,19000,19000]
assert sum(AREAS)==287000

# Published building-wise patterns. We slightly rescale MAPE/PICP/PINAW to honor the manuscript's headline
# aggregate values exactly/near-exactly despite small internal inconsistencies among rounded summary tables.
per_mape=pd.read_csv(ROOT/'results/per_building_mape.csv')
coverage=pd.read_csv(ROOT/'results/building_coverage_summary.csv')
MAPE_REPORTED=dict(zip(per_mape['Building'],per_mape['GBC-BEP']))
PICP_REPORTED=dict(zip(coverage['building_id'],coverage['picp_pct']))
PINAW_REPORTED=dict(zip(coverage['building_id'],coverage['pinaw']))
MAPE_SCALE=12.1/per_mape['GBC-BEP'].mean()
PICP_SHIFT=90.5-coverage['picp_pct'].mean()
PINAW_SCALE=0.319/coverage['pinaw'].mean()
MAPE_TARGET={b:MAPE_REPORTED[b]*MAPE_SCALE for b in BUILDINGS}
PICP_TARGET={b:PICP_REPORTED[b]+PICP_SHIFT for b in BUILDINGS}
PINAW_TARGET={b:PINAW_REPORTED[b]*PINAW_SCALE for b in BUILDINGS}

# Test calendar and the 12 synthetic excluded origins needed to obtain 4,380 origins from 4,392 candidates.
ALL_HOURS=pd.date_range('2022-07-01 00:00:00','2022-12-31 23:00:00',freq='h')
CANDIDATE_ORIGINS=pd.date_range('2022-07-01 00:00:00','2022-12-30 23:00:00',freq='h')
EXCLUDED=pd.DatetimeIndex(pd.to_datetime([
'2022-07-18 07:00:00','2022-08-04 13:00:00','2022-08-28 18:00:00',
'2022-09-14 09:00:00','2022-09-29 16:00:00','2022-10-12 11:00:00',
'2022-10-27 14:00:00','2022-11-09 08:00:00','2022-11-21 17:00:00',
'2022-12-02 10:00:00','2022-12-15 15:00:00','2022-12-27 12:00:00']))
ORIGINS=CANDIDATE_ORIGINS[~CANDIDATE_ORIGINS.isin(EXCLUDED)]
assert len(ORIGINS)==4380
ORIGIN_POS=ALL_HOURS.get_indexer(ORIGINS)
HORIZONS=np.tile(np.arange(1,25,dtype=np.int16),len(ORIGINS))
ORIGIN_REP_POS=np.repeat(ORIGIN_POS,24)
TARGET_POS=ORIGIN_REP_POS+HORIZONS
TARGET_TIMES=ALL_HOURS.values[TARGET_POS]
ORIGIN_TIMES=np.repeat(ORIGINS.values,24)
N_PER_BUILDING=len(HORIZONS)
assert N_PER_BUILDING==105120

# manuscript horizon/month interval summaries
hc=pd.read_csv(ROOT/'results/horizon_coverage_summary.csv')
HGRID=np.arange(1,25)
H_COV=np.interp(HGRID,hc['horizon_h'],hc['picp_pct'])
H_PINAW=np.interp(HGRID,hc['horizon_h'],hc['pinaw'])
mc=pd.read_csv(ROOT/'results/monthly_coverage_summary.csv')
MONTH_MAP={7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
M_COV={m:float(mc.loc[mc['month_2022']==name,'picp_pct'].iloc[0]) for m,name in MONTH_MAP.items()}
M_PINAW={m:float(mc.loc[mc['month_2022']==name,'pinaw'].iloc[0]) for m,name in MONTH_MAP.items()}
TARGET_MONTHS=pd.DatetimeIndex(TARGET_TIMES).month.to_numpy()

# ---------------- synthetic weather shared by campus ----------------
rng_weather=np.random.default_rng(SEED)
doy=ALL_HOURS.dayofyear.to_numpy(); hour=ALL_HOURS.hour.to_numpy(); dow=ALL_HOURS.dayofweek.to_numpy(); month=ALL_HOURS.month.to_numpy()
TEMP=19+11*np.cos(2*np.pi*(doy-205)/365.25)+4*np.sin(2*np.pi*(hour-14)/24)+rng_weather.normal(0,1.8,len(ALL_HOURS))
RH=np.clip(65-0.8*(TEMP-20)+rng_weather.normal(0,6,len(ALL_HOURS)),25,95)
GHI=np.maximum(0,650*np.sin(np.pi*np.clip((hour-6)/13,0,1)))
GHI*=0.75+0.25*np.cos(2*np.pi*(doy-172)/365.25)
GHI*=np.clip(rng_weather.normal(0.9,0.12,len(ALL_HOURS)),0.4,1.1)
WIND=np.clip(2.4+rng_weather.normal(0,1.0,len(ALL_HOURS)),0.1,8.5)

# Error-shape parameters tuned so aggregate synthetic metrics round to the paper's 56.8/40.5/12.1 and ~19.8% CV-RMSE.
LOAD_SCALE=1.1069217688431598
ERR_C0=3.25
ERR_BETA=0.24


def true_load_series(bid,btype,area,seed):
    rng=np.random.default_rng(seed)
    h=hour; wd=(dow<5); weekend=~wd
    if btype=='Lecture Hall':
        intensity=0.022
        prof=np.where(wd,0.28+0.80*((h>=8)&(h<=18))+0.18*np.exp(-((h-10)/2.0)**2)+0.13*np.exp(-((h-15)/2.2)**2),
                      0.26+0.22*((h>=9)&(h<=17)))
        prof*=np.where(month<=8,0.72,1.0)
    elif btype=='Research Lab':
        intensity=0.030
        prof=0.72+0.38*((h>=8)&(h<=20))+0.10*np.exp(-((h-13)/3.0)**2)
        prof*=np.where(weekend,0.88,1.0)
    elif btype=='Administrative Office':
        intensity=0.021
        prof=np.where(wd,0.20+1.02*((h>=8)&(h<=18))+0.10*np.exp(-((h-13)/2.8)**2),
                      0.18+0.15*((h>=9)&(h<=16)))
    else:
        intensity=0.018
        prof=0.26+0.35*((h>=8)&(h<=16))+0.95*((h>=17)&(h<=22))
        prof+=0.25*weekend*((h>=10)&(h<=21))
        ev=np.zeros(len(ALL_HOURS))
        event_days=rng.choice(np.unique(ALL_HOURS.normalize()),size=22,replace=False)
        for d in event_days:
            start=int(rng.integers(14,19)); dur=int(rng.integers(2,5))
            mask=(ALL_HOURS.normalize()==d)&(h>=start)&(h<start+dur)
            ev[mask]+=rng.uniform(0.6,1.4)
        prof+=ev
    cool=np.maximum(TEMP-24,0); heat=np.maximum(10-TEMP,0)
    weather=1+0.030*cool+0.018*heat
    drift=1+0.04*np.sin(2*np.pi*(np.arange(len(ALL_HOURS))/24)/(31*3))
    idfac=0.90+0.02*int(bid[1:])
    y=area*intensity*prof*weather*drift*idfac*LOAD_SCALE
    eps=rng.normal(0,0.035,len(ALL_HOURS)); eps=np.convolve(eps,np.ones(3)/3,mode='same')
    y*=np.clip(1+eps,0.85,1.2)
    return np.maximum(y,5.0)


def make_error(y_hourly,bid,seed):
    rng=np.random.default_rng(seed)
    yt=y_hourly[TARGET_POS]
    eps_b=0.01*np.median(y_hourly[y_hourly>0])
    med=np.median(yt)
    prev=y_hourly[np.maximum(TARGET_POS-1,0)]
    ramp=np.abs(yt-prev)/(np.median(y_hourly)+1e-6)
    hfac=0.86+0.012*HORIZONS
    z=np.abs(rng.normal(size=len(yt)))
    shape=(ERR_C0+z)*(np.maximum(yt/med,0.15)**ERR_BETA)*(1+0.08*np.minimum(ramp,2))*hfac
    q=shape*(MAPE_TARGET[bid]/100)/shape.mean()
    abs_err=q*(yt+eps_b)
    sign=np.where(rng.random(len(yt))<0.5,-1.0,1.0)
    err=sign*abs_err
    return yt,err,eps_b


def make_cover_mask(bid,seed):
    rng=np.random.default_rng(seed)
    cb=PICP_TARGET[bid]/100; base=0.905
    month_delta=np.array([logit(M_COV[m]/100)-logit(base) for m in TARGET_MONTHS])
    p=expit(logit(cb)+0.40*(logit(H_COV[HORIZONS-1]/100)-logit(base))+0.40*month_delta)
    u=np.clip(rng.random(len(p)),1e-12,1.0)
    score=-np.log(u)/(p/(1-p))
    k=int(round(cb*len(p)))
    idx=np.argpartition(score,k-1)[:k]
    mask=np.zeros(len(p),dtype=bool); mask[idx]=True
    return mask


def make_dispersion(abs_err,bid,seed):
    # Positive noisy surrogates designed to be moderately rank-correlated with realized absolute error.
    rng=np.random.default_rng(seed)
    mean=np.mean(abs_err)
    # A common absolute-error scale is used across buildings so between-building differences do not dominate the rank relation.
    global_sd=39.23
    n1=rng.normal(size=len(abs_err))
    n2i=rng.normal(size=len(abs_err))
    rho=0.20
    n2=rho*n1+np.sqrt(1-rho*rho)*n2i
    l1=abs_err+1.27*global_sd*n1
    l2=abs_err+1.08*global_sd*n2
    # Fixed positive offset preserves global ranks; multiplication yields a kWh^2-like magnitude.
    scale=40.0
    u1=np.maximum(l1+400.0,1e-6)*scale
    u2=np.maximum(l2+400.0,1e-6)*scale
    return u1,u2,u1+u2


def allocate_widths(yt,err,u_raw,bid,cover):
    abs_e=np.abs(err); yrange=float(yt.max()-yt.min())
    target_mean=float(PINAW_TARGET[bid]*yrange)
    target_total=target_mean*len(yt)
    # Bounds ensure the desired coverage mask when intervals are centered on y_pred.
    minw=np.where(cover,2*abs_e*1.004,2*abs_e*0.18)
    maxw=np.where(cover,np.inf,2*abs_e*0.992)
    if minw.sum()>target_total:
        # Should never occur with the manuscript's reported PINAW; retained as a safe fallback.
        minw=np.where(cover,2*abs_e*1.001,0.0)
    w=minw.copy()
    remaining=target_total-w.sum()
    if remaining < -1e-6:
        raise RuntimeError(f'PINAW target infeasible for {bid}')
    # Horizon/month/dispersion weighting preserves qualitative sharpness patterns.
    hrel=H_PINAW[HORIZONS-1]/np.mean(H_PINAW)
    mrel=np.array([M_PINAW[m] for m in TARGET_MONTHS]); mrel=mrel/np.mean(mrel)
    ur=(u_raw-np.min(u_raw))/(np.ptp(u_raw)+1e-12)
    weights=hrel*mrel*(0.78+0.44*ur)
    cap=maxw-w
    active=np.ones(len(w),dtype=bool)
    for _ in range(12):
        if remaining<=1e-7: break
        denom=weights[active].sum()
        if denom<=0: break
        proposal=np.zeros(len(w))
        proposal[active]=remaining*weights[active]/denom
        add=np.minimum(proposal,cap)
        gained=add.sum()
        w+=add; remaining-=gained; cap-=add
        active=np.isinf(cap)|(cap>1e-10)
        if gained<=1e-9: break
    if remaining>1e-5:
        # Covered intervals have no upper cap; distribute any numerical residual over them.
        cw=weights*cover
        w+=remaining*cw/cw.sum()
        remaining=0.0
    return w,yrange

# ---------------- metadata ----------------
floors=[5,4,6,4,5,5,4,6, 5,6,5,7,6,5,6, 6,5,7,6,7, 3,4,4]
year_band=['2000-2009','2000-2009','2010-2015','1990-1999','2010-2015','2000-2009','1990-1999','2016-2020',
           '2000-2009','2010-2015','2000-2009','2016-2020','2010-2015','2000-2009','2016-2020',
           '2000-2009','1990-1999','2010-2015','2000-2009','2016-2020','2000-2009','2010-2015','2016-2020']
hvac=[]
for t in TYPES:
    hvac.append({'Lecture Hall':'VAV + central chilled water','Research Lab':'VAV + central chilled water + extended-hours ventilation','Administrative Office':'VAV + central chilled water','Sports Facility':'AHU + central chilled water'}[t])
chw=[True]*23
hw=[False,False,True,False,True,False,False,True, True,True,True,True,True,True,True, False,True,False,True,False, True,True,True]
steam=[False]*8+[True,True,False,True,False,True,False]+[False]*5+[False,True,False]
meta=pd.DataFrame({
    'building_id':BUILDINGS,'functional_type':TYPES,'floor_area_m2':AREAS,'floors':floors,
    'construction_year_band':year_band,'primary_hvac_system':hvac,'electricity_meter_available':True,
    'chilled_water_meter_available':chw,'hot_water_meter_available':hw,'steam_meter_available':steam,
    'wifi_occupancy_proxy_available':True,'metadata_status':'synthetic_reconstruction_for_reproducibility'
})
meta.to_csv(META/'building_metadata.csv',index=False,encoding='utf-8-sig')

raw_vars=[
('electricity_kwh','Energy','Electricity sub-meter energy','kWh','sum','all buildings'),
('chilled_water_kwh','Energy','Chilled-water energy where metered','kWh','sum','subset'),
('hot_water_kwh','Energy','Hot-water energy where metered','kWh','sum','subset'),
('steam_kwh','Energy','Steam energy equivalent where metered','kWh','sum','subset'),
('outdoor_temp_c','Weather','Outdoor dry-bulb temperature','degC','mean','all buildings/shared weather'),
('relative_humidity_pct','Weather','Outdoor relative humidity','%','mean','all buildings/shared weather'),
('ghi_w_m2','Weather','Global horizontal irradiance','W/m2','mean','all buildings/shared weather'),
('wind_speed_m_s','Weather','Wind speed','m/s','mean','all buildings/shared weather'),
('wifi_occupancy_count','Occupancy','WiFi-derived occupancy proxy','count','mean','all buildings'),
('occupancy_schedule_state','Occupancy','Scheduled occupancy state','binary/categorical','mode','all buildings'),
('hvac_on_state','BMS','HVAC operational state','binary','mode','all buildings'),
('supply_air_temp_c','BMS','AHU supply-air temperature','degC','mean','where available'),
('return_air_temp_c','BMS','AHU return-air temperature','degC','mean','where available'),
('chw_supply_temp_c','BMS','Chilled-water supply temperature','degC','mean','where available'),
('chw_return_temp_c','BMS','Chilled-water return temperature','degC','mean','where available'),
('hw_supply_temp_c','BMS','Hot-water supply temperature','degC','mean','where available'),
('hw_return_temp_c','BMS','Hot-water return temperature','degC','mean','where available'),
('supply_airflow_m3_s','BMS','Supply airflow','m3/s','mean','where available'),
('fan_speed_pct','BMS','Fan command/speed','%','mean','where available'),
('damper_position_pct','BMS','Outdoor-air damper position','%','mean','where available'),
('cooling_valve_position_pct','BMS','Cooling-valve position','%','mean','where available'),
('heating_valve_position_pct','BMS','Heating-valve position','%','mean','where available'),
('indoor_temp_c','BMS','Representative indoor temperature','degC','mean','where available'),
('indoor_rh_pct','BMS','Representative indoor relative humidity','%','mean','where available'),
('co2_ppm','BMS','Representative indoor CO2 concentration','ppm','mean','where available'),
('zone_setpoint_c','BMS','Representative zone temperature set-point','degC','mean/mode','where available'),
('floor_area_m2','Building metadata','Anonymized floor area descriptor','m2','static','all buildings'),
('functional_type','Building metadata','Anonymized functional type','categorical','static','all buildings')]
rv=pd.DataFrame(raw_vars,columns=['variable','feature_group','description','unit_or_type','hourly_aggregation','availability'])
rv['release_status']='synthetic schema only; raw CAMPUS-REAL remains restricted'
rv.to_csv(META/'raw_variable_schema_28.csv',index=False,encoding='utf-8-sig')

# expanded public dictionary
dd=pd.DataFrame([
('building_id','Anonymized building identifier B01-B23','categorical','public/synthetic reproduction'),
('timestamp','Hourly target timestamp after 15-min to hourly aggregation','datetime','synthetic reproduction'),
('forecast_origin','Origin time for a 24-h forecast','datetime','synthetic reproduction'),
('horizon','Forecast horizon','hour 1-24','synthetic reproduction'),
('y_true','Synthetic observed target load constructed to match manuscript-scale behavior','kWh','synthetic only; NOT institutional measurement'),
('y_pred','Synthetic GBC-BEP point forecast','kWh','synthetic reproduction'),
('lower_90','Lower bound of synthetic calibrated 90% interval','kWh','synthetic reproduction'),
('upper_90','Upper bound of synthetic calibrated 90% interval','kWh','synthetic reproduction'),
('U_within','Synthetic within-state predictive-dispersion indicator','kWh^2-like score','synthetic reproduction'),
('U_between','Synthetic between-granule predictive-disagreement indicator','kWh^2-like score','synthetic reproduction'),
('U_raw','Sum of U_within and U_between','kWh^2-like score','synthetic reproduction'),
('raw_private_features','Energy/BMS/occupancy/weather source variables','mixed','restricted; not reconstructed as real records'),
('floor_area_m2','Synthetic anonymized floor area; portfolio total fixed to ~287,000 m2','m2','synthetic metadata'),
('floors','Synthetic structural descriptor','integer','synthetic metadata'),
('construction_year_band','Synthetic construction-vintage band','categorical','synthetic metadata'),
('primary_hvac_system','Synthetic HVAC descriptor consistent with building function','categorical','synthetic metadata')],
columns=['public_field','description','unit_or_type','release_status'])
dd.to_csv(META/'data_dictionary.csv',index=False,encoding='utf-8-sig')

# keep feature schema manuscript-aligned, with more explicit representative variables
fs=pd.DataFrame([
('Energy history','lags 1,2,3,24,48,168 h; first differences','history only; every lag is shifted before rolling operations'),
('Rolling statistics','mean/std over 6,24,168 h','computed only from shifted historical target values'),
('Calendar','hour/day cyclic encoding, month, weekend/holiday, working-hour state','deterministic from timestamp'),
('Weather','outdoor temperature, RH, GHI, wind speed','short gaps <=6 h interpolated; longer gaps use training-only conditioned medians'),
('Occupancy/BMS','WiFi occupancy proxy, schedules, HVAC/BMS states','hourly mean or modal state; missingness masks retained'),
('Building metadata','functional type, floor area, floors, vintage/HVAC descriptor when available','static; reproduction values marked synthetic')],
columns=['feature_group','representative_features','causal_rule'])
fs.to_csv(META/'feature_schema.csv',index=False,encoding='utf-8-sig')

# split file remains exactly aligned to manuscript
pd.DataFrame([
('CAMPUS-REAL','train','2020-01-01 00:00:00','2021-12-31 23:59:59'),
('CAMPUS-REAL','validation_calibration','2022-01-01 00:00:00','2022-06-30 23:59:59'),
('CAMPUS-REAL','test','2022-07-01 00:00:00','2022-12-31 23:59:59')],columns=['dataset','split','start','end']).to_csv(META/'split_timestamps.csv',index=False,encoding='utf-8-sig')

# origin availability audit
audit=pd.DataFrame({'forecast_origin':CANDIDATE_ORIGINS})
audit['target_end']=audit['forecast_origin']+pd.Timedelta(hours=24)
audit['full_24h_calendar_available']=True
audit['protected_target_mask_available']=~audit['forecast_origin'].isin(EXCLUDED)
audit['included_in_synthetic_reproduction']=audit['protected_target_mask_available']
audit['reason']=np.where(audit['included_in_synthetic_reproduction'],'included','synthetic protected-target availability exclusion (12 origins required by manuscript count)')
audit.to_csv(META/'origin_availability_audit.csv',index=False,encoding='utf-8-sig',date_format='%Y-%m-%d %H:%M:%S')

# ---------------- generate predictions ----------------
metrics=[]
ss=sa=sp=sy=0.0; n_total=0; cov_total=0
h_cov_count=np.zeros(24,dtype=np.int64); h_count=np.zeros(24,dtype=np.int64); h_width=np.zeros(24)
m_cov_count={m:0 for m in MONTH_MAP}; m_count={m:0 for m in MONTH_MAP}; m_width={m:0.0 for m in MONTH_MAP}
sample_abs=[]; sample_u1=[]; sample_u2=[]; sample_uraw=[]

for i,(bid,btype,area) in enumerate(zip(BUILDINGS,TYPES,AREAS)):
    y_hourly=true_load_series(bid,btype,area,1000+i)
    yt,err,eps_b=make_error(y_hourly,bid,9000+i)
    ypred=yt-err
    cover=make_cover_mask(bid,7000+i)
    u1,u2,uraw=make_dispersion(np.abs(err),bid,6000+i)
    widths,yrange=allocate_widths(yt,err,uraw,bid,cover)
    lower=ypred-widths/2; upper=ypred+widths/2
    actual_cover=(lower<=yt)&(yt<=upper)
    # Exact coverage should follow the designed mask.
    if not np.array_equal(actual_cover,cover):
        raise RuntimeError(f'coverage construction mismatch for {bid}')

    out=pd.DataFrame({
        'building_id':bid,
        'timestamp':pd.to_datetime(TARGET_TIMES).strftime('%Y-%m-%d %H:%M:%S'),
        'forecast_origin':pd.to_datetime(ORIGIN_TIMES).strftime('%Y-%m-%d %H:%M:%S'),
        'horizon':HORIZONS,
        'y_true':yt,'y_pred':ypred,'lower_90':lower,'upper_90':upper,
        'U_within':u1,'U_between':u2,'U_raw':uraw
    })
    out.to_csv(PRED/f'{bid}_predictions.csv',index=False,encoding='utf-8-sig',float_format='%.4f')

    rmse=float(np.sqrt(np.mean(err**2))); mae=float(np.mean(np.abs(err))); mape=float(100*np.mean(np.abs(err)/(yt+eps_b)))
    picp=float(100*np.mean(actual_cover)); pinaw=float(np.mean(widths)/yrange)
    metrics.append((bid,btype,len(yt),rmse,mae,mape,picp,pinaw,float(np.mean(yt)),float(yrange)))
    ss+=float(np.sum(err**2)); sa+=float(np.sum(np.abs(err))); sp+=float(np.sum(np.abs(err)/(yt+eps_b))); sy+=float(np.sum(yt)); n_total+=len(yt); cov_total+=int(actual_cover.sum())
    for h in range(1,25):
        m=(HORIZONS==h); h_cov_count[h-1]+=int(actual_cover[m].sum()); h_count[h-1]+=int(m.sum()); h_width[h-1]+=float(widths[m].sum())
    for mo in MONTH_MAP:
        m=(TARGET_MONTHS==mo); m_cov_count[mo]+=int(actual_cover[m].sum()); m_count[mo]+=int(m.sum()); m_width[mo]+=float(widths[m].sum())
    # systematic sample for correlation verification
    idx=np.arange(0,len(yt),21)
    sample_abs.append(np.abs(err)[idx]); sample_u1.append(u1[idx]); sample_u2.append(u2[idx]); sample_uraw.append(uraw[idx])

metrics_df=pd.DataFrame(metrics,columns=['building_id','functional_type','n_rows','rmse_kwh','mae_kwh','mape_pct','picp_pct','pinaw','mean_y_true_kwh','y_range_kwh'])
metrics_df.to_csv(META/'reproduction_building_metrics.csv',index=False,encoding='utf-8-sig',float_format='%.6f')

rmse=math.sqrt(ss/n_total); mae=sa/n_total; mape=100*sp/n_total; mean_y=sy/n_total; cv=100*rmse/mean_y; picp=100*cov_total/n_total; macro_pinaw=metrics_df['pinaw'].mean()
abs_s=np.concatenate(sample_abs); u1s=np.concatenate(sample_u1); u2s=np.concatenate(sample_u2); urs=np.concatenate(sample_uraw)
r1=float(spearmanr(abs_s,u1s).statistic); r2=float(spearmanr(abs_s,u2s).statistic); rr=float(spearmanr(abs_s,urs).statistic)
summary=pd.DataFrame([
('rows_total',n_total,'2,417,760'),('forecast_origins_per_building',len(ORIGINS),'4,380'),('horizon_hours',24,'24'),
('rmse_kwh',rmse,'56.8'),('mae_kwh',mae,'40.5'),('micro_mape_pct',mape,'12.1'),('cv_rmse_pct',cv,'19.8'),('picp_pct',picp,'90.5'),('macro_pinaw',macro_pinaw,'0.319'),
('spearman_U_within_abs_error',r1,'0.531 (paper target; synthetic is approximate)'),('spearman_U_between_abs_error',r2,'0.587 (paper target; synthetic is approximate)'),('spearman_U_raw_abs_error',rr,'0.648 (paper target; synthetic is approximate)')
],columns=['metric','synthetic_value','paper_reference'])
summary.to_csv(META/'reproduction_summary.csv',index=False,encoding='utf-8-sig')

hdf=pd.DataFrame({'horizon_h':HGRID,'synthetic_picp_pct':100*h_cov_count/h_count,'paper_picp_target_pct':H_COV,'synthetic_mean_width_kwh':h_width/h_count,'paper_pinaw_pattern':H_PINAW})
hdf.to_csv(META/'horizon_diagnostics.csv',index=False,encoding='utf-8-sig',float_format='%.6f')
mdf=pd.DataFrame([{'month_2022':MONTH_MAP[m],'synthetic_picp_pct':100*m_cov_count[m]/m_count[m],'paper_picp_target_pct':M_COV[m],'synthetic_mean_width_kwh':m_width[m]/m_count[m],'paper_pinaw_pattern':M_PINAW[m]} for m in MONTH_MAP])
mdf.to_csv(META/'monthly_diagnostics.csv',index=False,encoding='utf-8-sig',float_format='%.6f')

# provenance/notice files
notice=f'''# SYNTHETIC CAMPUS-REAL REPRODUCTION DATA\n\nThese files are deterministic **synthetic/reconstructed data for software and result-reproduction testing**. They are **not** the original CAMPUS-REAL measurements and must not be described or deposited as measured campus BMS/occupancy data.\n\nGeneration seed: {SEED}\n\nThe reconstruction follows the manuscript's public constraints: 23 anonymized buildings, approximately 287,000 m2 total floor area, the reported functional-type composition, July--December 2022 held-out period, 4,380 valid 24-h forecast origins per building, and 2,417,760 scalar building-origin-horizon prediction rows. Point-error magnitudes, building difficulty, empirical interval coverage and interval sharpness are calibrated to the manuscript's reported aggregate scale.\n\nBecause rounded manuscript summaries contain small internal inconsistencies, the generator prioritizes the headline CAMPUS-REAL results (RMSE 56.8 kWh, MAE 40.5 kWh, micro-MAPE 12.1%, CV-RMSE about 19.8%, PICP 90.5%, PINAW about 0.319) while preserving the relative building patterns in the supplied summary tables.\n\nRaw CAMPUS-REAL data remain restricted and are not reconstructed here.\n'''
(ROOT/'DATA_PROVENANCE.md').write_text(notice,encoding='utf-8')
(PRED/'README.md').write_text('''# CAMPUS-REAL synthetic timestamp-level predictions\n\n`B01_predictions.csv` through `B23_predictions.csv` contain deterministic synthetic/reconstructed values generated for reproducibility testing. They follow the manuscript schema and test-calendar size, but they are **not original CAMPUS-REAL measurements or final experimental exports**.\n\nRequired columns:\n`building_id,timestamp,forecast_origin,horizon,y_true,y_pred,lower_90,upper_90,U_within,U_between,U_raw`\n\nUse these files to exercise the code, regenerate diagnostics, and test figure/table pipelines. Do not cite them as institutional observations.\n''',encoding='utf-8')
(META/'DATA_PROVENANCE.md').write_text(notice,encoding='utf-8')

print(summary.to_string(index=False))
print('\nPer-building rows:',metrics_df['n_rows'].unique(),'total',metrics_df['n_rows'].sum())
print('\nHorizon diagnostics:')
print(hdf[['horizon_h','synthetic_picp_pct','paper_picp_target_pct']].to_string(index=False))
print('\nMonthly diagnostics:')
print(mdf[['month_2022','synthetic_picp_pct','paper_picp_target_pct']].to_string(index=False))
