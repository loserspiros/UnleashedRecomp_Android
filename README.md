<p align="center">
    <img src="https://raw.githubusercontent.com/hedge-dev/UnleashedRecompResources/refs/heads/main/images/logo/Logo.png" width="512"/>
</p>

<h1 align="center">Unleashed Recompiled: Android Edition</h1>

<p align="center">
  <strong>High-performance static recompilation of Sonic Unleashed (Xbox 360) running natively on Android, Linux, and Windows.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Android_|_Linux_|_Windows-blue?style=flat-square" alt="Platforms"/>
  <img src="https://img.shields.io/badge/Architecture-ARM64_|_x86--64-blue?style=flat-square" alt="Arch"/>
  <img src="https://img.shields.io/badge/Graphics-Vulkan_1.2-red?style=flat-square&logo=vulkan" alt="Vulkan"/>
  <img src="https://img.shields.io/badge/Status-Work_In_Progress-orange?style=flat-square" alt="Status"/>
</p>

---

This project is an **experimental, high-performance port** of [Sonic Unleashed Recompiled](https://github.com/hedge-dev/UnleashedRecomp). It utilizes static recompilation to translate Xbox 360 PowerPC instructions into native code, enabling the game to run with modern enhancements on Android (ARM64) as well as Linux and Windows (x86-64).

> [!IMPORTANT]
> **This repository does NOT contain any game assets.** You must provide your own legally acquired copy of *Sonic Unleashed* for the Xbox 360.

---

## ✨ Key Features & Enhancements

This fork introduces significant architectural improvements, "under-the-hood" performance optimizations, and multi-platform support:

### 🚀 Performance & Parallelism
- **Parallel Execution Engine:** Leverages C++17 parallel algorithms (`std::execution`) and Intel TBB to accelerate heavy tasks like asset size computation and GPU pipeline pre-compilation.
- **O(1) Achievement Lookups:** Refactored the Achievement Manager to use optimized hash-based lookups, eliminating redundant iteration overhead.
- **GPU Pipeline Optimization:** Highly optimized object iteration during shader pre-compilation to reduce stutter and improve load times.
- **Zero-Allocation File Parsing:** Optimized **STFS** and **SVOD** parsing to eliminate redundant string allocations and utilize memory-mapped I/O.
- **Thread-Local Mod Caching:** Implemented a thread-local lookup cache in the `ModLoader` to drastically reduce file system contention in modded environments.

### 🛠️ Architecture & Core
- **Modular Kernel:** The monolithic kernel has been refactored into modular units (`threading`, `synchronization`, `I/O`, `memory`) for superior stability and easier debugging.
- **Refactored Recompiler:** The instruction recompiler now uses a robust `RecompileArgs` architecture, improving code generation quality and maintainability.
- **Universal Save Redirection:** Seamlessly manages save data across different OSs and mod profiles.
- **Built-in Achievement System:** A native, faithfully recreated Xbox 360 Achievement Overlay and manager.

### 🎮 Mobile & Modern UX
- **Android:** Native ARM64 support with custom **Touch Controls**, Vulkan 1.2, and low-latency **AAudio/Oboe** backends.
- **Visual Enhancements:** Native support for **Resolution Scaling**, **Aspect Ratio Patches** (including Ultrawide support), and **High-Refresh-Rate** displays.
- **Controller Support:** Plug-and-play support for Xbox, PlayStation, and generic Bluetooth/HID controllers with dynamic icon switching.
- **Hedge Mod Manager:** Support for mods via standard community tools (limited on Android).

---

## 📱 Device Requirements (Android)

| Requirement | Minimum Specification | Recommended |
| :--- | :--- | :--- |
| **Architecture** | ARMv8-A 64-bit (ARM64) | Latest flagship SoC (Snapdragon 8 Gen 1+) |
| **OS Version** | Android 8.0 (API 26) | Android 11+ |
| **Graphics API** | Vulkan 1.2 | Vulkan 1.3 |
| **RAM** | 4 GB (Strict Guest Allocation) | 8 GB+ |
| **Storage** | 10 GB (Internal Storage) | 15 GB+ (UFS 3.1+) |

---

## 🚀 Getting Started

### 1. Prepare Your Assets
Create a `private/` directory in the project root and place the following:
- `default.xex` — The main game executable.
- `default.xexp` — Title update (optional).
- `shader.ar` — DLC or shader archives (optional).
- Game data containers (STFS/SVOD).

### 2. Build via GitHub Actions (Easy)
Our CI pipeline is designed for robustness and ease of use:
1. **Fork** this repository.
2. Go to the **Actions** tab and select the **Release** workflow.
3. Click **Run workflow** and select your target OS (**Android, Linux, or Windows**).
4. **Dynamic Data Input:** You can provide URLs for your assets. The workflow supports **ZIP, ISO, and XEX** formats and will automatically extract and prepare them.
5. Download the final artifact once the build completes.

### 3. Manual Build (Linux/Android)
#### 📦 Dependencies
- `gcc 13+`, `g++ 13+`, `cmake` (3.20+), `git`, `wget`, `unzip`
- `libtbb-dev` (Intel Threading Building Blocks — **REQUIRED** for parallel optimizations)
- **Java 17** (Temurin recommended)
- Android SDK & **NDK 25.2.9519653** (For Android builds)

#### 🛠️ Build Steps
```bash
# 1. Clone with submodules
git clone --recursive https://github.com/yourusername/UnleashedRecomp-Android.git
cd UnleashedRecomp-Android

# 2. Build host-side tools
chmod +x ./build_tools.sh
./build_tools.sh

# 3. Configure and Build
# For Android:
export ANDROID_NDK_HOME=/path/to/ndk
./build_android.sh

# For Linux:
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

---

## ⚖️ Disclaimer
*Unleashed Recompiled: Android Edition* is an unofficial fan-made project. It is not affiliated with, authorized, or endorsed by SEGA® or Sonic Team™. All trademarks belong to their respective owners.
