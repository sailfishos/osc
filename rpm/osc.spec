# osc plugin support
%global osc_plugin_dir %{_prefix}/lib/osc-plugins
# for obs source services
%global obsroot %{_prefix}/lib/obs
%global obs_srcsvc_dir %{obsroot}/service

Name:           osc
Summary:        Open Build Service Commander
Version:        1.5.1
Release:        0
License:        GPLv2+
URL:            https://github.com/openSUSE/osc
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.xz
#For SailfishOS
# $  i=1; for j in 0*patch; do printf "Patch%04d: %s\n" $i $j; i=$((i+1));done
Patch0001:      0001-Add-sb2install-support-to-osc.patch
Patch0002:      0002-Support-osc-copyprj-in-api-by-Islam-Amer-usage-osc-c.patch
Patch0003:      0003-Support-synchronous-copyproj.patch
Patch0004:      0004-Add-p-to-copyprj-to-enable-copying-of-prjconf.patch
Patch0005:      0005-Add-support-for-rebuild-and-chroot-only-in-build.-re.patch
Patch0006:      0006-Add-architecture-and-scheduler-maps.patch
Patch0007:      0007-Trap-any-kind-of-exception-during-plugin-parsing-eg-.patch
Patch0008:      0008-Fix-hdrmd5-check-of-downloaded-packages-from-DoD-rep.patch
Patch0009:      0009-Use-busybox-compatible-commands-for-completion.patch
BuildRequires:  python3-cryptography
BuildRequires:  python3-devel
BuildRequires:  python3-distro
BuildRequires:  python3-urllib3
BuildRequires:  rpm-python
Requires:       python3-cryptography
Requires:       python3-distro
Requires:       python3-lxml
Requires:       python3-urllib3
Requires:       rpm-python

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
%{py3_install}

%__mkdir_p %{buildroot}%{_localstatedir}/lib/osc-plugins
install -Dm0644 contrib/complete.sh %{buildroot}%{_datadir}/bash-completion/completions/osc
install -Dm0755 contrib/osc.complete %{buildroot}%{_datadir}/osc/complete

mkdir -p %{buildroot}%{obs_srcsvc_dir}
mkdir -p %{buildroot}%{osc_plugin_dir}
mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d/

# osc rpm macros
cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.osc <<EOM
%%obs_srcsvc_dir %{obs_srcsvc_dir}
%%osc_plugin_dir %{osc_plugin_dir}
EOM

%files
%doc AUTHORS README.md NEWS
%license COPYING
%{_bindir}/osc*
%{python3_sitelib}/osc*
%{_datadir}/bash-completion/completions/osc
%dir %{_localstatedir}/lib/osc-plugins
%{_datadir}/osc
%{_rpmconfigdir}/macros.d/macros.osc
%dir %{obsroot}
%dir %{obs_srcsvc_dir}
%dir %{osc_plugin_dir}
