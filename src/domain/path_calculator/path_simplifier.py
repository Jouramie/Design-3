from src.domain.environments.navigation_environment import NavigationEnvironment


class PathSimplifier(object):
    def __init__(self, navigation_environment: NavigationEnvironment):
        self.__navigation_environment = navigation_environment

    def simplify(self, original_path: [tuple]) -> [tuple]:
        simplified_path = original_path
        path_as_been_simplified = True

        while path_as_been_simplified:
            path_as_been_simplified, simplified_path = self._simplify_once(simplified_path)

        return simplified_path

    def _simplify_once(self, original_path: [tuple]) -> (bool, [tuple]):
        simplified_path = list(original_path)   # Create a copy
        path_as_been_simplified = False
        i = 0
        for j in range(1, len(original_path) - 1):
            k = j + 1
            if not self.__navigation_environment.is_crossing_obstacle([simplified_path[i], original_path[k]]):
                simplified_path.remove(original_path[j])
                path_as_been_simplified = True
            else:
                i += 1

        return path_as_been_simplified, simplified_path
