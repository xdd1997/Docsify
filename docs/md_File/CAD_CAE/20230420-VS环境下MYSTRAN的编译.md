





## 安装 Microsoft Visual Studio (Community 2019)

略，可参考 https://www.yuque.com/xdd1997/gbrnie/lg5morm6mgf6woez

蓝奏云：[vs_community_2019.exe](https://xdd1997.lanzoub.com/ikTHw0s9atli)

## 安装 Intel Fortran compiler

略，可参考 https://www.yuque.com/xdd1997/gbrnie/lg5morm6mgf6woez



## 编译 SuperLU 与 BLAS

项目构建时选择 Release x64

项目属性不需要添加包含目录

编译这两个库的原因是因为mystran求解时需要这两个库

1. 下载 [https://github.com/xiaoyeli/superlu/releases/tag/v5.3.0](https://github.com/xiaoyeli/superlu/releases/tag/v5.3.0) ，解压后重命名得到文件夹 superlu_530
2. 下载 [slu_Cnames.zip](https://xdd1997.lanzoub.com/iKwxG0s5pywf) 文件，解压后替换掉原来 superlu_530/SRC 与 superlu_530/CBLAS中的 slu_Cnames.h 文件
3. VS---新建项目--- C++ ---Windows桌面向导---下一步---项目名称为：SuperLU---创建---应用程序类型：静态库(.lib) --- 空项目 --- 确定

1. 1. 在项目右键---添加---现有项---将 superlu_530/SRC 中的代码加入项目，将 superlu_530/FORTRAN 中的4个 .c 文件加入到项目
   2. 改成 Release  x64
   3. 项目属性 --- C/C++ --- 常规 --- SDL 检查 --- 否
   4. 项目属性 --- C/C++ --- 预处理器 --- 预处理器定义 --- 加入：_CRT_SECURE_NO_WARNINGS
   5. 项目属性 --- VC++目录 --- 常规 ---包含目录 --- 将 superlu_530/SRC 的绝对路径加上**(有时不加也行，有时不加会报告** No such file or directory**)**
   6. 生成---生成解决方案，得到 SuperLU.lib

1. VS---新建项目--- C++ ---Windows桌面向导---下一步---项目名称为：BLAS ---创建---应用程序类型：静态库(.lib) ---空项目---确定

1. 1. 在项目右键---添加---现有项---将 superlu_530/CBLAS 中的代码加入项目
   2. 改成 Release x64
   3. 生成---生成解决方案，得到 BLAS.lib



## 编译 MYSTRAN.exe

这个项目最终会得到 MYSTRAN.exe 程序，可用来测试代码完整性与分析代码

1. 下载源码：[https://github.com/MYSTRANsolver/MYSTRAN_Releases](https://github.com/MYSTRANsolver/MYSTRAN_Releases)，  解压后得到14.01/Source/MYSTRAN-main_10_1_2022.zip/Source 文件夹，重命名为 Source_14
2. VS---新建项目---Fortran---Empty Project---下一步---项目名称：MYSTRAN---创建
3. 在项目右键---添加---Existing Items From Folder...---将 Source_14 中的代码加入项目
4. 在项目 Source Files 右键---添加---现有项---将 Source_14/MAIN/GET_INI_FILNAM.F90 加入项目
5. 在项目 Resource Files 右键---添加---现有项---将 SuperLU.lib 与 BLAS.lib 加入项目
6. 项目属性---配置与平台修改为 Debug x64
7. 项目属性---Fortran---Diagnostics---Check Routine Interfaces---No
8. 项目属性---Fortran---Gereral---Additional Include Directories 中添加 Source_14/INCLUDE 文件夹的绝对路径，如：D:\Desktop\Source_14\INCLUDE **（有时可以不加）**
9. 修改 TPLT2.f90 文件，删除560行多余的1个右括号，不然会有警告 #8043
10. 修改 GET_MYSTRAN_DIR.f90 文件，注释掉第44行，不然会有错误 #6407
11. 修改 WRITE_BAR.f90 文件，删除第48行的 `, INTENT(IN)`
12. 生成---生成解决方案，得到 MYSTRAN.exe