Name:		unetbootin
Version:	0
%define	gitdate	20110804
Release:	0.%{gitdate}.1
Summary:	Create bootable Live USB drives for a variety of Linux distributions
Group:		System/Configuration/Hardware
License:	GPLv2+
URL:		http://unetbootin.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{gitdate}.tar.xz
Patch0:		unetbootin-20110804-mdkconf.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# Syslinux is only available on x86 architectures
ExclusiveArch:	%{ix86} x86_64

BuildRequires:	desktop-file-utils
BuildRequires:	qt4-devel
# Not picked up automatically, required for operation
Requires:	p7zip
Requires:	syslinux

%description
UNetbootin allows you to create bootable Live USB drives for a variety of
Linux distributions from Windows or Linux, without requiring you to burn a CD.
You can either let it download one of the many distributions supported
out-of-the-box for you, or supply your own linux .iso file if you've already
downloaded one or your preferred distribution isn't on the list.

%prep
%setup -q -n %{name}-%{gitdate}
%patch0 -p1 -b .mdkconf~

# fix desktop file
sed -i '/^version/d' src/unetbootin/unetbootin.desktop
sed -i '/\[en_us\]/d' src/unetbootin/unetbootin.desktop
sed -i 's|/usr/bin/unetbootin|unetbootin|g' src/unetbootin/unetbootin.desktop

%build
cd src/unetbootin/

sed -i '/^RESOURCES/d' unetbootin.pro
lupdate unetbootin.pro
lrelease unetbootin.pro
qmake "DEFINES += NOSTATIC" "RESOURCES -= unetbootin.qrc"
make %{?_smp_mflags}

%install
rm -rf %{buildroot} 
install -D -p -m 755 src/unetbootin/unetbootin %{buildroot}%{_bindir}/unetbootin
install -d -m755 %{buildroot}%{_datadir}/unetbootin/
# Install desktop file
desktop-file-install --vendor="" --remove-category=Application --dir=%{buildroot}%{_datadir}/applications src/unetbootin/unetbootin.desktop
install -c -p -m 644 src/unetbootin/unetbootin_*.qm %{buildroot}%{_datadir}/unetbootin/

%find_lang unetbootin

%clean
rm -rf %{buildroot}

%files -f unetbootin.lang
%defattr(-,root,root,-)
%doc readme
%{_bindir}/unetbootin
%{_datadir}/unetbootin/
%{_datadir}/applications/unetbootin.desktop

