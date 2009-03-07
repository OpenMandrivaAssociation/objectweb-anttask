%define section         free
%define gcj_support     1

Summary:        ObjectWeb Ant task
Name:           objectweb-anttask
Version:        1.3.2
Release:        %mkrel 3.0.4
Epoch:          0
Group:          Development/Java
License:        LGPL
URL:            http://forge.objectweb.org/projects/monolog/
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Source0:        http://download.fr2.forge.objectweb.org/monolog/ow_util_ant_tasks_%{version}.tar.bz2
Patch0:         objectweb-anttask-1.3.2-filesets.patch
BuildRequires:  ant
BuildRequires:  java-rpmbuild
BuildRequires:  xalan-j2
BuildRequires:  asm2
Provides:       owanttask = %{epoch}:%{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
ObjectWeb Ant task

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -c -q -n %{name}
%patch0 -p1
%remove_java_binaries

%build
export CLASSPATH=$(build-classpath xalan-j2 asm2/ )
export OPT_JAR_LIST=:
%{ant} jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 output/lib/ow_util_ant_tasks.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
  ln -sf %{name}-%{version}.jar %{name}.jar
popd

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a output/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
