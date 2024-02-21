try:
    import internal.loader as loader
    loader.main()
    
except Exception as exception:
    import internal.recovery as recovery
    recovery.system_recovery(exception)
