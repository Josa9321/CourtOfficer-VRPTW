import vrptw

if __name__ == "__main__":
    parse_args = vrptw.get_parse_args()
    instance = vrptw.load_json_instance(parse_args.instance)

    solution = vrptw.solve_instance(instance, parse_args.verbose)
    solution.save("solution_" + parse_args.instance)
    if parse_args.google == 1:
        solution.print_route_in_google(instance)
