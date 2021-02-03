import sys
import swsearch
import swsearch.cli
import swsearch.config
import swsearch.log
import swsearch.task


def main(args=None, with_logging=True):
    if args is None:
        args = sys.argv[1:]

    if not args:
        args = ['--help']

    if with_logging:
        swsearch.log.configure_logging(debug=False)

    parser = swsearch.cli.get_parser()
    args = parser.parse_args(args)
    config = swsearch.config.load_config(args.config)

    try:
        swsearch.task.search(config, args.search_term)
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
