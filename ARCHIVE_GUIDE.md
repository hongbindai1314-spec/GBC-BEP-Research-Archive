# GBC-BEP Research Archive

## 数据来源与适用范围 / Data provenance

本档案合并用户提供的 19 个压缩包，规范目录、文件名称和路径引用，保留数据数值及来源说明。正式归档格式不改变数据的性质或验证状态。

原始说明将校园时序、预测数组、EnergyPlus 输入及 BDG2 六站点数据描述为生成或模拟重建材料，用于代码、流程与指标复现测试。它们不能视为原始校园观测、官方 BDG2 子集、官方气象文件或原始实验结果。部分结果汇总来自所提供的论文修订表格；本次仅校验归档完整性，没有验证论文结论、运行模型或确认真实数据来源。

The supplied documentation identifies campus series and predictions, EnergyPlus inputs, and the six-site BDG2 material as synthetic/reconstructed research assets. Neutral filenames do not change this provenance. Consult the local README and DATA_PROVENANCE files for dataset-specific limitations. Reported validation results are inherited from the source archives and were not independently rerun.

## Contents

- `campus_dataset/`: campus time series and alignment audits.
- `campus_real_metadata/`: building metadata and diagnostics.
- `predictions/`, `baseline_predictions/`: prediction arrays.
- `bdg2/`: six-site benchmark material and audits.
- `energyplus/`: model inputs, weather, schedules and benchmark assets.
- `src/`, `scripts/`, `configs/`: implementation and configuration.
- `results/`: supplied numerical summaries.

## Packaging

Identical repeated files were merged. Python bytecode caches were omitted. Data arrays were not regenerated. Human-readable file references were updated to match renamed files; scientific provenance statements and computational logic were retained. Source filenames remain in `archive_manifest.csv` for traceability. `SHA256SUMS.txt` covers every packaged file except itself. Original ZIP files were left unchanged.
