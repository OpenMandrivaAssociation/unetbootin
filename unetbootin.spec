%global rel 393

Name:		unetbootin
Version:	0
Release:	%mkrel 0.%{rel}bzr
Summary:	Create bootable Live USB drives for a variety of Linux distributions
Group:		System/Configuration/Hardware
License:	GPLv2+
URL:		http://unetbootin.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-source-%{rel}.tar.gz
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
out-of-the-box for you, or supply your own Linux .iso file if you've already
downloaded one or your preferred distribution isn't on the list.

%prep
%setup -q -c 
# Fix EOL encoding
for file in README.TXT; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done
# Fix desktop file
sed -i '/^Version/d' unetbootin.desktop
sed -i '/\[en_US\]/d' unetbootin.desktop
sed -i 's|/usr/bin/unetbootin|unetbootin|g' unetbootin.desktop

%build

# Ugh, there's no macro for running lrelease and on RHEL the default is qt-3.3
%if 0%{?rhel} == 5
# Generate .qm files
%{_libdir}/qt4/bin/lrelease unetbootin.pro
%{_libdir}/qt4/bin/qmake
%else
# Generate .qm files
lrelease unetbootin.pro
qmake
%endif

make %{?_smp_mflags}

%install
rm -rf %{buildroot} 
install -D -p -m 755 unetbootin %{buildroot}%{_bindir}/unetbootin
# Install desktop file
desktop-file-install --vendor="" --remove-category=Application --dir=%{buildroot}%{_datadir}/applications unetbootin.desktop
# Install localization files
install -d %{buildroot}%{_datadir}/unetbootin
install -c -p -m 644 unetbootin_*.qm %{buildroot}%{_datadir}/unetbootin/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.TXT
%{_bindir}/unetbootin
%{_datadir}/unetbootin/
%{_datadir}/applications/unetbootin.desktop

