from collections import defaultdict
from backend.models.event_log import EventLog
from backend.models.process_model import ProcessModel
from backend.models.conformance_result import ConformanceResult, Deviation

class ConformanceService:
    def check_conformance(self, model: ProcessModel, log: EventLog) -> ConformanceResult:
        """
        Performs conformance checking using token replay on a DFG.

        Args:
            model: The discovered process model (DFG).
            log: The event log to check against the model.

        Returns:
            A ConformanceResult object with fitness and a list of deviations.
        """
        deviations = []
        total_activities = len(log.events)
        fitting_activities = 0

        # For efficient lookup
        model_edges = {(edge.source, edge.target) for edge in model.edges}
        model_nodes = {node.id for node in model.nodes}

        # Group events by case and sort by timestamp
        cases = defaultdict(list)
        for event in log.events:
            cases[event.case_id].append(event)

        for case_id, events in cases.items():
            events.sort(key=lambda e: e.timestamp)
            
            if not events:
                continue

            # Replay the trace
            for i, event in enumerate(events):
                activity_name = event.activity_name

                if activity_name not in model_nodes:
                    deviations.append(Deviation(
                        case_id=case_id,
                        activity_name=activity_name,
                        deviation_type="Unseen Activity",
                        timestamp=event.timestamp
                    ))
                    continue # This activity can't be part of a fitting edge either

                # Check transition
                if i > 0:
                    prev_activity_name = events[i-1].activity_name
                    if (prev_activity_name, activity_name) in model_edges:
                        fitting_activities += 1
                    else:
                        deviations.append(Deviation(
                            case_id=case_id,
                            activity_name=activity_name,
                            deviation_type="Unexpected Transition",
                            timestamp=event.timestamp
                        ))
                else: # First event in the trace
                    # In this simple model, we count the first event as fitting if the activity exists.
                    fitting_activities += 1

        # Calculate fitness
        fitness = fitting_activities / total_activities if total_activities > 0 else 1.0

        return ConformanceResult(fitness=fitness, deviations=deviations)

conformance_service = ConformanceService()
