
/* usr/src/cmd/zpool/zpool_main.c */

/*
 * Print out detailed scrub status.
 */
void
print_scan_status(pool_scan_stat_t *ps)
{
	time_t start, end;
	uint64_t elapsed, mins_left, hours_left;
	uint64_t pass_exam, examined, total;
	uint_t rate;
	double fraction_done;
	char processed_buf[7], examined_buf[7], total_buf[7], rate_buf[7];

	(void) printf(gettext("  scan: "));

	/* If there's never been a scan, there's not much to say. */
	if (ps == NULL || ps->pss_func == POOL_SCAN_NONE ||
	    ps->pss_func >= POOL_SCAN_FUNCS) {
		(void) printf(gettext("none requested\n"));
		return;
	}

	start = ps->pss_start_time;
	end = ps->pss_end_time;
	zfs_nicenum(ps->pss_processed, processed_buf, sizeof (processed_buf));

	assert(ps->pss_func == POOL_SCAN_SCRUB ||
	    ps->pss_func == POOL_SCAN_RESILVER);
	/*
	 * Scan is finished or canceled.
	 */
	if (ps->pss_state == DSS_FINISHED) {
		uint64_t minutes_taken = (end - start) / 60;
		char *fmt = NULL;

		if (ps->pss_func == POOL_SCAN_SCRUB) {
			fmt = gettext("scrub repaired %s in %lluh%um with "
			    "%llu errors on %s");
		} else if (ps->pss_func == POOL_SCAN_RESILVER) {
			fmt = gettext("resilvered %s in %lluh%um with "
			    "%llu errors on %s");
		}
		/* LINTED */
		(void) printf(fmt, processed_buf,
		    (u_longlong_t)(minutes_taken / 60),
		    (uint_t)(minutes_taken % 60),
		    (u_longlong_t)ps->pss_errors,
		    ctime((time_t *)&end));
		return;
	} else if (ps->pss_state == DSS_CANCELED) {
		if (ps->pss_func == POOL_SCAN_SCRUB) {
			(void) printf(gettext("scrub canceled on %s"),
			    ctime(&end));
		} else if (ps->pss_func == POOL_SCAN_RESILVER) {
			(void) printf(gettext("resilver canceled on %s"),
			    ctime(&end));
		}
		return;
	}

	assert(ps->pss_state == DSS_SCANNING);

	/*
	 * Scan is in progress.
	 */
	if (ps->pss_func == POOL_SCAN_SCRUB) {
		(void) printf(gettext("scrub in progress since %s"),
		    ctime(&start));
	} else if (ps->pss_func == POOL_SCAN_RESILVER) {
		(void) printf(gettext("resilver in progress since %s"),
		    ctime(&start));
	}

	examined = ps->pss_examined ? ps->pss_examined : 1;
	total = ps->pss_to_examine;
	fraction_done = (double)examined / total;

	/* elapsed time for this pass */
	elapsed = time(NULL) - ps->pss_pass_start;
	elapsed = elapsed ? elapsed : 1;
	pass_exam = ps->pss_pass_exam ? ps->pss_pass_exam : 1;
	rate = pass_exam / elapsed;
	rate = rate ? rate : 1;
	mins_left = ((total - examined) / rate) / 60;
	hours_left = mins_left / 60;

	zfs_nicenum(examined, examined_buf, sizeof (examined_buf));
	zfs_nicenum(total, total_buf, sizeof (total_buf));
	zfs_nicenum(rate, rate_buf, sizeof (rate_buf));

	/*
	 * do not print estimated time if hours_left is more than 30 days
	 */
	(void) printf(gettext("    %s scanned out of %s at %s/s"),
	    examined_buf, total_buf, rate_buf);
	if (hours_left < (30 * 24)) {
		(void) printf(gettext(", %lluh%um to go\n"),
		    (u_longlong_t)hours_left, (uint_t)(mins_left % 60));
	} else {
		(void) printf(gettext(
		    ", (scan is slow, no estimated time)\n"));
	}

	if (ps->pss_func == POOL_SCAN_RESILVER) {
		(void) printf(gettext("    %s resilvered, %.2f%% done\n"),
		    processed_buf, 100 * fraction_done);
	} else if (ps->pss_func == POOL_SCAN_SCRUB) {
		(void) printf(gettext("    %s repaired, %.2f%% done\n"),
		    processed_buf, 100 * fraction_done);
	}
}
