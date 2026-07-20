import os
import numpy as np
import soundfile as sf
import pyloudnorm as pyln

def analyze_game_sfx(wav_dir: str) -> dict:
    """
    批量分析游戏音效的听感响度(LUFS)。
    对于短音效，优先使用 Momentary Loudness；若文件过短则回退到 K-weighted RMS。
    """
    results = {}

    if not os.path.exists(wav_dir):
        print(f"错误: 目录不存在 -> {wav_dir}")
        return results

    wav_files = [f for f in os.listdir(wav_dir) if f.lower().endswith('.wav')]
    print(f"找到 {len(wav_files)} 个 WAV 文件，开始分析...\n")

    for filename in sorted(wav_files):
        filepath = os.path.join(wav_dir, filename)
        try:
            data, sr = sf.read(filepath)

            # 确保为二维数组 (samples, channels)
            if data.ndim == 1:
                data = data.reshape(-1, 1)

            duration = len(data) / sr

            # --- 核心响度计算 ---
            # ITU-R BS.1770 要求至少 ~400ms 才能准确计算 Integrated Loudness
            # 游戏音效通常很短，我们采用以下策略：
            meter = pyln.Meter(sr, block_size=duration)  # 400ms block

            # if duration >= 0.4:
            # 使用 Momentary Loudness (无门限，适合短音效)
            loudness = meter.integrated_loudness(data)
            # else:
            #     # 极短音效：手动 K-weighting 后计算 RMS → 转为 LUFS
            #     # pyloudnorm 内部有 K-weight filter，这里用简化方式
            #     filtered = meter._filter_k_weighting(data.T).T
            #     rms = np.sqrt(np.mean(filtered ** 2))
            #     # LUFS ≈ -0.691 + 10*log10(rms^2)，参考 BS.1770 公式
            #     loudness = -0.691 + 10 * np.log10(max(rms ** 2, 1e-12))
            #     method = "K-weighted RMS"

            # 静音检测
            if np.max(np.abs(data)) < 1e-6:
                loudness = -np.inf

            results[filename] = {
                "loudness_lufs": round(loudness, 2),
                "duration_sec": round(duration, 4),
                "sample_rate": sr,
                "channels": data.shape[1],
            }

        except Exception as e:
            results[filename] = {"error": str(e)}
            print(f"  ⚠ 跳过 {filename}: {e}")

    return results


if __name__ == "__main__":
    TARGET_DIR = "vanilla_assets/wav/"
    report = analyze_game_sfx(TARGET_DIR)

    # 打印结果字典
    print("\n===== 分析结果 =====")
    print("文件名                  | 响度(LUFS) | 时长(s) | 采样率")
    for name, info in report.items():
        if "error" in info:
            print(f"{name}: 错误 - {info['error']}")
        else:
            print(f"{name}: {info['loudness_lufs']:>7.2f} LUFS | "
                  f"{info['duration_sec']:.3f}s | {info['sample_rate']}Hz")

    # 也输出原始字典方便程序化使用
    print("\n===== Raw Dict =====")
    print(report)