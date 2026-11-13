# Data excluded from this edition

The folder was assembled using an explicit allowlist: three Python modules and five HTML templates. It did not copy participant folders, questionnaire CSVs, alert logs, session JSONs, recordings, virtual environments, or original `.git` history. The full study report is omitted so that individual-level tables or embedded outputs are not inadvertently redistributed.

The source metadata JSON in `docs/` contains file hashes and origin information only. No original participant records are used as test fixtures. Tests use the literal synthetic label `SYNTHETIC_DEMO` and a temporary directory outside the repository.

`.gitignore` excludes runtime data folders, participant-style folders, CSV/JSON exports, recordings, environment files and caches. This protects against accidental additions; it does not sanitize files or prevent force-adding them. Review the exact upload contents again after conducting any new session.

The running app still supports registration, age/gender fields, questionnaire collection and local saving because those are features of the study tool. Removing historic participant data does not disable collection of new records. The shared in-memory state and global video/audio resources assume a single local user.
