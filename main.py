import logging
import sys
from scanner.network_scan import scan_runner
from healthchecks.healthchecker import healthcheck_runner

# Logger config

logging.basicConfig(
	level = logging.INFO,
	format = '%(asctime)s - %(levelname)s - %(message)s',
	handlers = [
		logging.FileHandler('toolkit.log'),
		logging.StreamHandler(sys.stdout)
	])

logger = logging.getLogger("toolkit")

def main():
	logger.info("Starting Network Scan")
	target_cidr = input("Please enter the target CIDR:")
	scan_runner(target_cidr)
	logger.info("Finished Network Scan")

	logger.info("Starting Healthchecks")
	healthcheck_runner()
	logger.info("Finished Healthchecks")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\nScan interrupted by user (Ctrl+C)")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Unhandled fatal error: {e}")
        logger.exception("Stacktrace complete:")
        sys.exit(1)
