from collections import defaultdict
from backend.models.event_log import EventLog
from backend.models.process_model import ProcessModel, Node, Edge

class DFGDiscovery:
    def discover(self, log: EventLog) -> ProcessModel:
        """
        Discovers a Directly-Follows Graph (DFG) from an event log.
        """
        dfg = defaultdict(int)
        activity_counts = defaultdict(int)
        
        # Group events by case_id and sort by timestamp
        cases = defaultdict(list)
        for event in log.events:
            cases[event.case_id].append(event)
        
        for case_id in cases:
            cases[case_id].sort(key=lambda x: x.timestamp)

        # Build DFG and count activities
        for case_id, events in cases.items():
            if not events:
                continue
            
            # Count first activity
            activity_counts[events[0].activity_name] += 1

            for i in range(len(events) - 1):
                source_activity = events[i].activity_name
                target_activity = events[i+1].activity_name
                dfg[(source_activity, target_activity)] += 1
                activity_counts[target_activity] += 1
        
        # Create nodes and edges for the process model
        nodes = [Node(id=activity, label=activity, size=count) for activity, count in activity_counts.items()]
        edges = [Edge(source=source, target=target, weight=weight) for (source, target), weight in dfg.items()]

        return ProcessModel(nodes=nodes, edges=edges)

dfg_discovery_service = DFGDiscovery()
