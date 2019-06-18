/*
-E : exit on error and issue error message and code.


*/

//ERRORS:

/*VARARGS*/
//https://github.com/file/file/blob/09e4e370538bcb52ebfd74b32e09fc85aec1f4b0/src/funcs.c#L99
__attribute__((__format__(__printf__, 3, 0)))
private void
file_error_core(struct magic_set *ms, int error, const char *f, va_list va,
    size_t lineno)
{
	/* Only the first error is ok */
	if (ms->event_flags & EVENT_HAD_ERR)
		return;
	if (lineno != 0) {
		free(ms->o.buf);
		ms->o.buf = NULL;
		(void)file_printf(ms, "line %" SIZE_T_FORMAT "u:", lineno);
	}
	if (ms->o.buf && *ms->o.buf)
		(void)file_printf(ms, " ");
	(void)file_vprintf(ms, f, va);
	if (error > 0)
		(void)file_printf(ms, " (%s)", strerror(error));
	ms->event_flags |= EVENT_HAD_ERR;
	ms->error = error;
}
//https://github.com/file/file/blob/7d8deea23d3fc8d5ffc571e9dbe469c7b1cfa809/src/fsmagic.c#L297
#ifdef	S_IFLNK
	case S_IFLNK:
		if ((nch = readlink(fn, buf, BUFSIZ-1)) <= 0) {
			if (ms->flags & MAGIC_ERROR) {
			    file_error(ms, errno, "unreadable symlink `%s'",
				fn);
			    return -1;
			}
			if (mime) {
				if (handle_mime(ms, mime, "symlink") == -1)
					return -1;
			} else if (silent) {
			} else if (file_printf(ms,
			    "%sunreadable symlink `%s' (%s)", COMMA, fn,
			    strerror(errno)) == -1)
				return -1;
			break;
		}
		buf[nch] = '\0';	/* readlink(2) does not do this */

		/* If broken symlink, say so and quit early. */
#ifdef __linux__
		/*
		 * linux procfs/devfs makes symlinks like pipe:[3515864880]
		 * that we can't stat their readlink output, so stat the
		 * original filename instead.
		 */
		if (stat(fn, &tstatbuf) < 0)
			return bad_link(ms, errno, buf);
#else
		if (*buf == '/') {
			if (stat(buf, &tstatbuf) < 0)
				return bad_link(ms, errno, buf);
		} else {
			char *tmp;
			char buf2[BUFSIZ+BUFSIZ+4];

			if ((tmp = strrchr(fn,  '/')) == NULL) {
				tmp = buf; /* in current directory anyway */
			} else {
				if (tmp - fn + 1 > BUFSIZ) {
					if (ms->flags & MAGIC_ERROR) {
						file_error(ms, 0,
						    "path too long: `%s'", buf);
						return -1;
					}
					if (mime) {
						if (handle_mime(ms, mime,
						    "x-path-too-long") == -1)
							return -1;
					} else if (silent) {
					} else if (file_printf(ms,
					    "%spath too long: `%s'", COMMA,
					    fn) == -1)
						return -1;
					break;
				}
				/* take dir part */
				(void)strlcpy(buf2, fn, sizeof buf2);
				buf2[tmp - fn + 1] = '\0';
				/* plus (rel) link */
				(void)strlcat(buf2, buf, sizeof buf2);
				tmp = buf2;
			}
			if (stat(tmp, &tstatbuf) < 0)
				return bad_link(ms, errno, buf);
		}
#endif

// ...


if (ret) {
	if (ms->flags & MAGIC_ERROR) {
		file_error(ms, errno, "cannot stat `%s'", fn);
		return -1;
	}
	if (file_printf(ms, "cannot open `%s' (%s)",
	    fn, strerror(errno)) == -1)
		return -1;
	return 0;
}

ret = 1;

//https://github.com/file/file/blob/818e82a83c2f14833763d99a3e5d5457678f3bf5/src/apptype.c#L87
#if 0
	if (rc == ERROR_INVALID_EXE_SIGNATURE)
		printf("%s: not an executable file\n", fname);
	else if (rc == ERROR_FILE_NOT_FOUND)
		printf("%s: not found\n", fname);
	else if (rc == ERROR_ACCESS_DENIED)
		printf("%s: access denied\n", fname);
	else if (rc != 0)
		printf("%s: error code = %lu\n", fname, rc);
	else
