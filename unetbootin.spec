%global rel 581
%define debug_package %{nil}

Name:		unetbootin
Version:	0
Release:	2.%{rel}
Summary:	Create bootable Live USB drives for a variety of Linux distributions
Group:		System/Configuration/Hardware
License:	GPLv2+
URL:		http://unetbootin.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-source-%{rel}.tar.gz
Patch1:		rosa-config.patch
# Syslinux is only available on x86 architectures
ExclusiveArch:	%{ix86} x86_64

BuildRequires:	desktop-file-utils
BuildRequires:	qt4-devel
# Not picked up automatically, required for operation
#Requires:	extlinux
Requires:	p7zip
Requires:	syslinux
Requires:	usermode

%description
UNetbootin allows you to create bootable Live USB drives for a variety of
Linux distributions from Windows or Linux, without requiring you to burn a CD.
You can either let it download one of the many distributions supported
out-of-the-box for you, or supply your own Linux .iso file if you've already
downloaded one or your preferred distribution isn't on the list.


%prep
%setup -q -c
%apply_patches

%build
mv unetbootin.desktop rosa-unetbootin.desktop
lupdate unetbootin.pro
lrelease unetbootin.pro
qmake

%make


%install
rm -rf %{buildroot} 
install -D -p -m 755 unetbootin %{buildroot}%{_sbindir}/unetbootin
# Install desktop file
desktop-file-install --vendor="" --remove-key=Version --remove-key=Name[en_US] --remove-key=GenericName[en_US] --remove-key=Comment[en_US] --remove-category=Application --dir=%{buildroot}%{_datadir}/applications rosa-unetbootin.desktop
# Install localization files
install -d %{buildroot}%{_datadir}/unetbootin
install -c -p -m 644 unetbootin_*.qm %{buildroot}%{_datadir}/unetbootin/
# Install icons
install -D -c -p -m 644 unetbootin_16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_22.png %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_24.png %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_64.png %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_192.png %{buildroot}%{_datadir}/icons/hicolor/192x192/apps/unetbootin.png
install -D -c -p -m 644 unetbootin_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/unetbootin.png

# setup link for consolehelper support to allow root access
install -d %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s consolehelper %{name}
popd


%files
%doc README.TXT
%{_bindir}/unetbootin
%{_sbindir}/unetbootin
%{_datadir}/unetbootin/
%{_datadir}/applications/rosa-unetbootin.desktop
%{_datadir}/icons/hicolor/*/*




%changelog

* Tue Sep 18 2012 sander85 <sander85> 0-2.581.mga3
+ Revision: 295942
- New release: 581

* Mon Jul 23 2012 sander85 <sander85> 0-2.578.mga3
+ Revision: 273726
- new release: 578

* Sat Mar 03 2012 sander85 <sander85> 0-2.568.mga2
+ Revision: 217224
- new version

* Sat Jan 07 2012 sander85 <sander85> 0-2.563.mga2
+ Revision: 193008
- new release: 563

* Fri Oct 07 2011 sander85 <sander85> 0-2.555.mga2
+ Revision: 152719
- add extlinux as a requirement as it was splitted from syslinux

* Thu Oct 06 2011 sander85 <sander85> 0-1.555.mga2
+ Revision: 152211
- switch to tarball source

* Sat Oct 01 2011 sander85 <sander85> 0-0.555.mga2
+ Revision: 150665
- fix bug #1443
- new version: 555

* Sat Apr 30 2011 sander85 <sander85> 0-0.549.mga1
+ Revision: 93728
- imported package unetbootin

