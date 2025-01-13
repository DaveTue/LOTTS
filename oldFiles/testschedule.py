#Service definition

from collections import defaultdict, deque

class cosimSchedule:
    def __init__(self, relationships=dict()):
        self.relationships = relationships
        print(relationships)
        self.graph = self.dependency_graph()
        self.schedule, self.cycle = self.handle_cycles()

    def dependency_graph(self) -> dict:
        graph = defaultdict(list)

        for element, dependenOn in self.relationships.items():
            dependants = list(dependenOn.keys())

            for dependant in dependants:
                graph[element].append(dependant)

        return graph

    def add_node(self, node):
        """Adds a node to the dependency graph."""
        if node not in self.graph:
            self.graph[node] = []

    def add_dependency(self, node, dependency):
        """Adds a dependency for a given node."""
        self.add_node(node)
        self.add_node(dependency)
        self.graph[node].append(dependency)

    def find_strongly_connected_components(self):
        """Finds strongly connected components (SCCs) using Tarjan's algorithm."""
        index = 0
        stack = []
        indices = {}
        lowlinks = {}
        on_stack = set()
        sccs = []

        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlinks[node] = index
            index += 1
            stack.append(node)
            on_stack.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
                elif neighbor in on_stack:
                    lowlinks[node] = min(lowlinks[node], indices[neighbor])

            if lowlinks[node] == indices[node]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    scc.append(w)
                    if w == node:
                        break
                sccs.append(scc)

        # Create a list of keys to avoid modifying the graph while iterating
        for node in list(self.graph.keys()):
            if node not in indices:
                strongconnect(node)

        return sccs

    def handle_cycles(self):
        """Handles cycles in the dependency graph by resolving SCCs and removing minimal edges."""
        sccs = self.find_strongly_connected_components()
        print(f"Found SCCs: {sccs}")

        acyclic_graph = defaultdict(list)
        scc_map = {}

        # Map each node to its SCC index
        for i, scc in enumerate(sccs):
            for node in scc:
                scc_map[node] = i

        # Build an acyclic graph of SCCs
        for node in self.graph:
            for neighbor in self.graph[node]:
                if scc_map[node] != scc_map[neighbor]:
                    acyclic_graph[scc_map[node]].append(scc_map[neighbor])

        print(f"Initial acyclic graph of SCCs: {acyclic_graph}")

        resolved_sccs = {}
        removed_edges = []

        # Resolve each SCC
        for i, scc in enumerate(sccs):
            if len(scc) > 1:  # Only resolve cycles for SCCs with more than one node
                resolved_order = self.resolve_cycle(scc, removed_edges)
                resolved_sccs[i] = resolved_order
            else:
                resolved_sccs[i] = scc

        # Update the acyclic graph by replacing SCCs with resolved orders
        updated_acyclic_graph = defaultdict(list)
        for scc_index, neighbors in acyclic_graph.items():
            for neighbor in neighbors:
                updated_acyclic_graph[scc_index].append(neighbor)

        print(f"Updated acyclic graph: {updated_acyclic_graph}")

        # Check for remaining cycles in the updated graph
        try:
            sorted_sccs = self.topological_sort(updated_acyclic_graph)
        except ValueError as e:
            print(f"Error during topological sort: {e}")
            raise ValueError("Graph contains irreducible cycles.")

        print(f"Topologically sorted SCCs: {sorted_sccs}")

        # Generate the final schedule
        schedule = []
        for scc_index in sorted_sccs:
            schedule.extend(resolved_sccs[scc_index])

        print(f"Final schedule: {schedule}")
        return schedule, [scc for scc in sccs if len(scc) > 1]

    def resolve_cycle(self, cycle, removed_edges):
        """Resolves a cycle by removing edges iteratively until the cycle is broken."""
        cycle_graph = {node: [neighbor for neighbor in self.graph[node] if neighbor in cycle] for node in cycle}
        print(f"Resolving cycle: {cycle}")
        print(f"Initial cycle graph: {cycle_graph}")

        while self.has_cycle_after_removal(cycle_graph):
            for node in list(cycle_graph):
                if cycle_graph[node]:  # If the node has neighbors
                    neighbor = cycle_graph[node].pop(0)  # Remove the first neighbor
                    removed_edges.append((node, neighbor))
                    print(f"Removed edge: {node} -> {neighbor}")

                    if not self.has_cycle_after_removal(cycle_graph):
                        break

        sorted_cycle = self.topological_sort(cycle_graph)
        print(f"Resolved cycle into order: {sorted_cycle}")
        return sorted_cycle

    def has_cycle_after_removal(self, graph):
        """Checks for a cycle in a modified graph."""
        visited = set()
        stack = set()

        def visit(node):
            if node in stack:
                return True  # Cycle detected
            if node in visited:
                return False

            visited.add(node)
            stack.add(node)
            for neighbor in graph[node]:
                if visit(neighbor):
                    return True
            stack.remove(node)
            return False

        for node in graph:
            if visit(node):
                return True
        return False

    def topological_sort(self, graph=None):
        """Performs a topological sort on the dependency graph."""
        if graph is None:
            graph = self.graph

        # Initialize in_degree for all nodes
        in_degree = {node: 0 for node in graph}
        for node in graph:
            for dependency in graph[node]:
                if dependency not in in_degree:
                    in_degree[dependency] = 0
                in_degree[dependency] += 1

        # Collect nodes with no incoming edges
        queue = deque([node for node in in_degree if in_degree[node] == 0])
        sorted_order = []

        while queue:
            node = queue.popleft()
            sorted_order.append(node)

            for dependency in graph.get(node, []):
                in_degree[dependency] -= 1
                if in_degree[dependency] == 0:
                    queue.append(dependency)

        if len(sorted_order) != len(graph):
            raise ValueError("Graph has a cycle, topological sort not possible.")

        return sorted_order
class cosimSchedule2:
    def __init__(self, relationships = dict()):
        self.relationships =  relationships
        print(relationships)
        # self.graph = defaultdict(list)
        self.graph = self.dependency_graph()
        self.cycleFlag = self.has_cycle()
        
        if self.cycleFlag:
            self.cycle = self.find_cycle()
            sorted_order, removed_edges =self.suggest_sort_with_cycle()
            self.schedule = sorted_order
            self.compRemoved = removed_edges
        else:
            self.schedule = self.topological_sort()
            self.cycle = []
    
    def dependency_graph(self)-> dict:
        graph = defaultdict(list)
            
        for element, dependenOn in self.relationships.items():
            dependants = list(dependenOn.keys()) 
           
            for dependant in dependants:
                graph[element].append(dependant)
                
        return graph
    
    def add_node(self, node):
        """Adds a node to the dependency graph."""
        if node not in self.graph:
            self.graph[node] = []

    def add_dependency(self, node, dependency):
        """Adds a dependency for a given node."""
        self.add_node(node)
        self.add_node(dependency)
        self.graph[node].append(dependency)

    def has_cycle(self):
        """Detects if there is a cycle in the graph using DFS."""
        visited = set()
        stack = set()

        def visit(node):
            if node in stack:
                return True  # Cycle detected
            if node in visited:
                return False

            visited.add(node)
            stack.add(node)
            for neighbor in self.graph[node]:
                if visit(neighbor):
                    return True
            stack.remove(node)
            return False

        for node in self.graph:
            if visit(node):
                return True
        return False

    def find_cycle(self):
        """Finds and returns the elements involved in a cycle, if any."""
        visited = set()
        stack = []
        cycle = []

        def dfs(node):
            if node in stack:
                cycle_start_index = stack.index(node)
                cycle.extend(stack[cycle_start_index:])
                return True
            if node in visited:
                return False

            visited.add(node)
            stack.append(node)

            for neighbor in self.graph[node]:
                if dfs(neighbor):
                    return True

            stack.pop()
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    break

        return cycle

    def suggest_sort_with_cycle(self):
        """Suggests a topological sort by removing the minimum edges to break cycles."""
        cycle = self.find_cycle()

        if not cycle:
            return self.topological_sort()  # No cycle, return regular topological sort

        # Remove the minimum edges to break the cycle
        graph_copy = {node: neighbors[:] for node, neighbors in self.graph.items()}

        min_removed_edges = []
        for i in range(len(cycle)):
            src = cycle[i]
            dest = cycle[(i + 1) % len(cycle)]  # Next node in the cycle
            if dest in graph_copy[src]:
                graph_copy[src].remove(dest)
                min_removed_edges.append((src, dest))

                if not self.has_cycle_after_removal(graph_copy):
                    break

        # Perform topological sort on the modified graph
        return self.topological_sort(graph_copy), min_removed_edges

    def has_cycle_after_removal(self, graph):
        """Checks for a cycle in a modified graph."""
        visited = set()
        stack = set()

        def visit(node):
            if node in stack:
                return True  # Cycle detected
            if node in visited:
                return False

            visited.add(node)
            stack.add(node)
            for neighbor in graph[node]:
                if visit(neighbor):
                    return True
            stack.remove(node)
            return False

        for node in graph:
            if visit(node):
                return True
        return False

    def topological_sort(self, graph=None):
        """Performs a topological sort on the dependency graph."""
        if graph is None:
            graph = self.graph

        in_degree = {node: 0 for node in graph}
        for node in graph:
            for dependency in graph[node]:
                in_degree[dependency] += 1

        # Collect nodes with no incoming edges
        queue = deque([node for node in graph if in_degree[node] == 0])
        sorted_order = []

        while queue:
            node = queue.popleft()
            sorted_order.append(node)

            for dependency in graph[node]:
                in_degree[dependency] -= 1
                if in_degree[dependency] == 0:
                    queue.append(dependency)

        if len(sorted_order) != len(graph):
            raise ValueError("Graph has a cycle, topological sort not possible.")
        sorted_order.reverse()
        return sorted_order
    
# Example Usage
relationships = {
    'Gain_model': {'UnitChange':None},
    'UnitChange': {'Transformator467': None, 'Gain_model': None},
    'Transformator467': {'Gain_model':None},
    'MassSpringDamperModel': {'Transformator1': None,'Transformator2': None,'Transformator3': None},
    'Transformator1': {'Gain_model': None},
    'Transformator2': {'Gain_model': None},
    'Transformator3': {'Gain_model': None}
}

scheduler = cosimSchedule2(relationships)
print("Schedule:", scheduler.schedule)
print("Cycles:", scheduler.cycle)
