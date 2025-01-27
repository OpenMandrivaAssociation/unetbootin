Name:		unetbootin
Version:	702
Release:	5
Summary:	Create bootable Live USB drives for a variety of Linux distributions
Group:		System/Configuration/Hardware
License:	GPLv2+
URL:		https://unetbootin.github.io/
Source0:	https://github.com/unetbootin/unetbootin/releases/download/%{version}/unetbootin-source-%{version}.tar.gz
Source1:	org.openmandriva.unetbootin.policy
Source2:	org.openmandriva.unetbootin.rules
Patch0:         %{name}-desktop.patch
Patch1:		unetbootin-702-pkexec.patch

BuildRequires:	desktop-file-utils
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-devel
BuildRequires:	qmake5
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)

# Not picked up automatically, required for operation
Requires:	(7zip or p7zip)
Requires:	polkit
Recommends:	extlinux
Recommends:	syslinux

%description
UNetbootin allows you to create bootable Live USB drives for a variety of
Linux distributions from Windows or Linux, without requiring you to burn a CD.
You can either let it download one of the many distributions supported
out-of-the-box for you, or supply your own Linux .iso file if you've already
downloaded one or your preferred distribution isn't on the list.


%prep
%setup -q -c
%autopatch -p1

%build
export QMAKE=%{_bindir}/qmake-qt5
%{_libdir}/qt5/bin/lupdate -pro *.pro
%{_libdir}/qt5/bin/lrelease *.pro
qmake-qt5 *.pro

%make_build


%install
rm -rf %{buildroot} 
install -D -m 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/%{name}

install -D -m 0644 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop


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

# PK integration
mkdir -p %{buildroot}%{_datadir}/polkit-1/{actions,rules.d}
cp %{S:1} %{buildroot}%{_datadir}/polkit-1/actions/
cp %{S:2} %{buildroot}%{_datadir}/polkit-1/rules.d/

%files
%doc README.TXT
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/unetbootin.desktop
%{_datadir}/icons/hicolor/*/*
%{_datadir}/polkit-1/actions/*
%{_datadir}/polkit-1/rules.d/*
