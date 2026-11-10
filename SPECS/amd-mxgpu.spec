%define vendor_name AMD
%define vendor_label amd
%define driver_name mxgpu

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 9.3.0.K
Release: .1.0.mxgpu.2
License: MIT
Source0: MxGPU-Virtualization-9.3.0.K.tar.gz

Patch0: 0001-Make-it-compile-on-4.19-kernel.patch
Patch1: 0002-Dont-report-Xen-dom0-as-a-guest-it-s-the-host.patch

BuildRequires: devtoolset-11-gcc
BuildRequires: kernel-devel
BuildRequires: autoconf
BuildRequires: automake
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n MxGPU-Virtualization-9.3.0.K

%build
source /opt/rh/devtoolset-11/enable
export EXTRA_CFLAGS='-DVERSION=\"%version\"'
export KSRC=/lib/modules/%{kernel_version}/build
export KVERSION=%{kernel_version}
export KERNELDIR=${KSRC}
cd gim; make

%install
# Cleanup unnecessary kernel-generated module dependency files.
find . -iname 'modules.*' -exec rm {} \;

mkdir -p %{buildroot}/lib/modules/%{kernel_version}/%{module_dir}
# mark modules executable so that strip-to-file can strip them
find . -name "*.ko" -type f -exec chmod u+x '{}' \;
find . -name "*.ko" -exec mv '{}' %{buildroot}/lib/modules/%{kernel_version}/%{module_dir} \;

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Thu Nov 04 2026 Yann Sionneau <yann.sionneau@vates.tech> - 9.3.0.K.1
- First import of AMD MxGPU release 9.3.0.K
