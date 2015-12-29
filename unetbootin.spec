%global rel 613

Name:		unetbootin
Version:	0
Release:	4.%{rel}
Summary:	Create bootable Live USB drives for a variety of Linux distributions
Group:		System/Configuration/Hardware
License:	GPLv2+
URL:		http://unetbootin.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-source-%{rel}.tar.gz
Patch1:		clang.patch
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
export CC=gcc
export CXX=g++

lupdate unetbootin.pro
lrelease unetbootin.pro
qmake

%make


%install
rm -rf %{buildroot} 
install -D -p -m 755 unetbootin %{buildroot}%{_sbindir}/unetbootin
# Install desktop file
desktop-file-install --vendor="" --remove-key=Version --remove-key=Name[en_US] --remove-key=GenericName[en_US] --remove-key=Comment[en_US] --remove-category=Application --dir=%{buildroot}%{_datadir}/applications unetbootin.desktop
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
install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_sysconfdir}/security/console.apps

ln -sf consolehelper %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_sysconfdir}/pam.d/%{name} <<EOF
#%PAM-1.0
auth            include         config-util
account         include         config-util
session         include         config-util
EOF

cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<EOF
USER=root
PROGRAM=/usr/sbin/%{name}
FALLBACK=false
SESSION=true
EOF

%files
%doc README.TXT
%{_bindir}/unetbootin
%{_sbindir}/unetbootin
%{_datadir}/unetbootin/
%{_datadir}/applications/unetbootin.desktop
%{_datadir}/icons/hicolor/*/*
%{_sysconfdir}/pam.d/%{name}
%{_sysconfdir}/security/console.apps/%{name}
