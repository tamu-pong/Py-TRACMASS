
VariantDir('build', 'source')
SConscriptChdir(True)
SConscript('build/SConscript')

Command('tracmass/_tracmass.so','build/_tracmass.so',
        Copy('$TARGET', '$SOURCE'))
#SConscript('source/SConstruct',variant_dir='build', duplicate=True)