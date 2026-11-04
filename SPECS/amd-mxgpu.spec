%define vendor_name AMD
%define vendor_label amd
%define driver_name mxgpu

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 9.3.0.K
Release: .1.0.mxgpu.1
License: MIT
Source0: MxGPU-Virtualization-9.3.0.K.tar.gz

Patch0: 0001-Make-it-compile-on-4.19-kernel.patch
Patch1: 0002-Dont-report-Xen-dom0-as-a-guest-it-s-the-host.patch

BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
export EXTRA_CFLAGS='-DVERSION=\"%version\"'
export KSRC=/lib/modules/%{kernel_version}/build
export KVERSION=%{kernel_version}
cd gim; make

%install
# Cleanup unnecessary kernel-generated module dependency files.
find %{buildroot}/lib/modules -iname 'modules.*' -exec rm {} \;

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -exec mv '{}' %{buildroot}/lib/modules/%{kernel_version}/%{module_dir} \;
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

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
