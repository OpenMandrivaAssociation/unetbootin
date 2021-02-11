%global rel 702

Name:		unetbootin
Version:	702
Release:	1
Summary:	Create bootable Live USB drives for a variety of Linux distributions
Group:		System/Configuration/Hardware
License:	GPLv2+
URL:		http://unetbootin.sourceforge.net/
Source0:	https://github.com/unetbootin/unetbootin/releases/download/%{rel}/unetbootin-source-%{rel}.tar.gz

BuildRequires:	desktop-file-utils
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-devel
BuildRequires:	qmake5
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)

# Not picked up automatically, required for operation
Recommends:	extlinux
Requires:	p7zip
Recommends:	syslinux
Requires:	usermode

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

%make


%install
rm -rf %{buildroot} 
install -D -p -m 0755 %{name} %{buildroot}%{_libexecdir}/%{name}

# Install desktop file
desktop-file-install --vendor="" \
	--remove-key=Version \
	--remove-key=Name[en_US] \
	--remove-key=GenericName[en_US] \
	--remove-key=Comment[en_US] \
	--remove-category=Application \
	--set-key=Exec --set-value=%{name} \
	--dir=%{buildroot}%{_datadir}/applications \
	unetbootin.desktop

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

# Policy Kit support for nice root access
%__mkdir_p %{buildroot}%{_bindir}
cat >%{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
if  [[ "\$UID" != "0" ]] ; then
    %{_bindir}/pkexec %{_libexecdir}/%{name} "\$@"
    exit \$?
fi
exec %{_libexecdir}/%{name} "\$@"
EOF

%files
%doc README.TXT
%attr(0755,root,root) %{_bindir}/%{name}
%{_libexecdir}/%{name}
%{_datadir}/unetbootin/
%{_datadir}/applications/unetbootin.desktop
%{_datadir}/icons/hicolor/*/*
%{_sysconfdir}/security/console.apps/%{name}
