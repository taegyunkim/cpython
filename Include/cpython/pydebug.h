#ifndef Py_LIMITED_API
#ifndef Py_PYDEBUG_H
#define Py_PYDEBUG_H
#ifdef __cplusplus
extern "C" {
#endif

/* this is a wrapper around getenv() that pays attention to
   Py_IgnoreEnvironmentFlag.  It should be used for getting variables like
   PYTHONPATH and PYTHONHOME from the environment */
PyAPI_FUNC(char*) Py_GETENV(const char *name);

/* Return process-global, read-only debugging metadata registered as name.
   Store its size in *size. Return NULL and store zero if name is unavailable.
   The returned pointer remains valid for the lifetime of the process. */
PyAPI_FUNC(const void *) PyUnstable_Debug_GetMetadata(
    const char *name,
    size_t *size);

#ifdef __cplusplus
}
#endif
#endif /* !Py_PYDEBUG_H */
#endif /* Py_LIMITED_API */
