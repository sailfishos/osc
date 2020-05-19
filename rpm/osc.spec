# osc plugin support
%global osc_plugin_dir %{_prefix}/lib/osc-plugins
# for obs source services
%global obsroot %{_prefix}/lib/obs
%global obs_srcsvc_dir %{obsroot}/service

Name:           osc
Summary:        Open Build Service Commander
Version:        0.168.2
Release:        0
License:        GPLv2+
URL:            https://github.com/openSUSE/osc
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.xz
#For SailfishOS
Patch0201:      0201-Add-sb2install-support-to-osc.patch
Patch0202:      0202-Support-osc-copyprj-in-api-by-Islam-Amer.patch
Patch0203:      0203-Support-synchronous-copyproj.patch
Patch0204:      0204-Add-p-to-copyprj-to-enable-copying-of-prjconf.patch
Patch0205:      0205-Add-support-for-rebuild-and-chroot-only-in-build.patch
Patch0206:      0206-Add-architecture-and-scheduler-maps.patch
Patch0207:      0207-Trap-any-kind-of-exception-during-plugin-parsing-eg-.patch
Patch0208:      0208-Fixup-old-style-print-statements.patch

BuildRequires:  python3-devel	
BuildRequires:  python3-distro
BuildRequires:  rpm-python
Requires:       python3-distro
Requires:       rpm-python
Requires:       python-m2crypto
Requires:       python3-lxml

%description
Commandline client for the Open Build Service. 
See http://en.opensuse.org/openSUSE:OSC, as well as
http://en.opensuse.org/openSUSE:Build_Service_Tutorial for a general
introduction.

%prep	
%autosetup -p1 -n %{name}-%{version}/osc

%build
%{py3_build}

%install
rm -rf %{buildroot}
%{py3_install}

%__ln_s osc-wrapper.py %{buildroot}%{_bindir}/osc
%__mkdir_p %{buildroot}%{_localstatedir}/lib/osc-plugins
install -Dm0644 dist/complete.sh %{buildroot}%{_datadir}/bash-completion/completions/osc
install -Dm0755 dist/osc.complete %{buildroot}%{_datadir}/osc/complete

mkdir -p %{buildroot}%{obs_srcsvc_dir}
mkdir -p %{buildroot}%{osc_plugin_dir}	
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/

# osc rpm macros
cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.osc <<EOM
%%obs_srcsvc_dir %{obs_srcsvc_dir}
%%osc_plugin_dir %{osc_plugin_dir}
EOM

%files
%doc AUTHORS README TODO NEWS
%license COPYING
%{_bindir}/osc*
%{python3_sitelib}/osc*
%{_datadir}/bash-completion/completions/osc
%dir %{_localstatedir}/lib/osc-plugins
%{_mandir}/man1/osc.*
%{_datadir}/osc
%{_rpmconfigdir}/macros.d/macros.osc
%dir %{obsroot}
%dir %{obs_srcsvc_dir}
%dir %{osc_plugin_dir}

