"""Maintained chapter membership and section types."""
REVISION="2026-10-22-narrative-guides"
BASELINE="c3d6f2dafdd87e083989135690e2f4f169e80fc2"
CHAPTERS={'devops': [{'slug': 'model',
             'title': 'Service architecture',
             'purpose': 'The service separates durable configuration from operational executions. This '
                        'chapter establishes those objects before following their connections to '
                        'evidence and retained knowledge.',
             'sections': ['D-01']},
            {'slug': 'access',
             'title': 'Data sources and integration configuration',
             'purpose': 'An investigation can use only the evidence exposed through its configured '
                        'access paths. Start with the supported connection families, then distinguish '
                        'operator roles, provider authorization, selected tools, and private routing.',
             'sections': ['D-12', 'D-02', 'D-03', 'D-04']},
            {'slug': 'knowledge',
             'title': 'Knowledge and execution context',
             'purpose': 'Current observations and retained information play different roles in a '
                        'diagnosis. Discovery builds an environment model; learning produces memories; '
                        'instructions and skills supply guidance. The following sections explain their '
                        'producers and retrieval paths.',
             'sections': ['D-05', 'D-M08', 'D-M01', 'D-M02', 'D-M07', 'D-M03', 'D-M04']},
            {'slug': 'operations',
             'title': 'Incident response and operational work',
             'purpose': 'With access and context configured, a signal can be routed into an '
                        'investigation or a defined operational task. This chapter follows execution, '
                        'observation, and the additional controls required for computation or '
                        'state-changing actions.',
             'sections': ['D-06', 'D-07', 'D-M05', 'D-M06', 'D-08', 'D-09']},
            {'slug': 'example',
             'title': 'Recurring-alarm analysis',
             'purpose': 'The same symptom can have a different cause in a later incident. The following '
                        'synthetic evidence shows how a useful investigation challenges historical '
                        'context with current measurements.',
             'sections': ['D-U01']},
            {'slug': 'diagnosis',
             'title': 'Troubleshooting and operating limits',
             'purpose': 'Failures can occur before analysis begins: identity, routing, tool selection, '
                        'and quotas all matter. Diagnose the first failed prerequisite before changing '
                        'the investigation hypothesis.',
             'sections': ['D-10']},
            {'slug': 'evidence',
             'title': 'Documentation coverage',
             'purpose': 'The references identify the documented behaviors used in this guide and the '
                        'procedures that remain linked rather than reproduced.',
             'sections': ['D-11']}],
 'security': [{'slug': 'model',
               'title': 'Service architecture',
               'purpose': 'The application space, assessment configuration, and run have different '
                          'responsibilities. Establishing that model makes later findings and '
                          'revalidation records interpretable.',
               'sections': ['S-01']},
              {'slug': 'access',
               'title': 'Application sources and target access',
               'purpose': 'Application evidence and a reachable test target are separate prerequisites. '
                          'The source inventory is followed by user access and the explicit boundaries '
                          'of a dynamic test.',
               'sections': ['S-09', 'S-02', 'S-03']},
              {'slug': 'mechanisms',
               'title': 'Application knowledge and assessment criteria',
               'purpose': 'Source context explains the application, requirements supply criteria, and '
                          'authentication provides a reachable identity. Their reuse mechanisms differ '
                          'and are described separately.',
               'sections': ['S-M07', 'S-M01', 'S-M02', 'S-M03', 'S-M04', 'S-M06']},
              {'slug': 'operations',
               'title': 'Assessment and finding workflows',
               'purpose': 'A run produces findings under particular conditions. Proposed changes, '
                          'deployed revisions, and subsequent verification remain linked but distinct '
                          'steps in the engineering workflow.',
               'sections': ['S-04', 'S-05', 'S-M05', 'S-06']},
              {'slug': 'example',
               'title': 'Authorization-finding analysis',
               'purpose': 'The synthetic example follows one account-authorization defect from the '
                          'original observation to a deployed repair and scoped revalidation.',
               'sections': ['S-U01']},
              {'slug': 'diagnosis',
               'title': 'Troubleshooting and operating limits',
               'purpose': 'An incomplete assessment may reflect an inaccessible source, failed '
                          'authentication, a wrong criterion, or an execution limit. These cases '
                          'require different corrective actions.',
               'sections': ['S-07']},
              {'slug': 'evidence',
               'title': 'Documentation coverage',
               'purpose': 'The source register separates documented product behavior from authored '
                          'engineering examples and identifies linked procedures.',
               'sections': ['S-08']}],
 'finops': [{'slug': 'model',
             'title': 'Service architecture',
             'purpose': 'The instance persists configuration and context; conversations and tasks '
                        'perform individual pieces of work. The resource model explains which state '
                        'belongs to each.',
             'sections': ['F-01']},
            {'slug': 'access',
             'title': 'Cost-data sources and collaboration connections',
             'purpose': 'A cost conclusion depends on its source data and query basis. Collaboration '
                        'destinations add a separate publication path with its own authorization and '
                        'lifecycle.',
             'sections': ['F-08', 'F-02', 'F-M01', 'F-05']},
            {'slug': 'context',
             'title': 'Organizational knowledge and session context',
             'purpose': 'Uploaded mappings, retained preferences, and summarized conversations are '
                        'different representations of organizational context. The operator must know '
                        'which representation to correct.',
             'sections': ['F-M02', 'F-M03', 'F-M04']},
            {'slug': 'operations',
             'title': 'Tasks, reporting, and data lifecycle',
             'purpose': 'Requests and automations create executions; executions produce results and '
                        'artifacts. This chapter follows that sequence through publication and the '
                        'supported retention controls.',
             'sections': ['F-03', 'F-M05', 'F-04', 'F-M06', 'F-M07']},
            {'slug': 'example',
             'title': 'Cost-variance analysis',
             'purpose': 'The synthetic example reconciles the monetary change before using limited '
                        'operational evidence to explain only part of it.',
             'sections': ['F-U01']},
            {'slug': 'diagnosis',
             'title': 'Troubleshooting and operating limits',
             'purpose': 'A numerical disagreement, a missing task, and a failed publication are '
                        'different faults. Troubleshooting follows the corresponding data, execution, '
                        'and destination paths.',
             'sections': ['F-06']},
            {'slug': 'evidence',
             'title': 'Documentation coverage',
             'purpose': 'The references document the source, context, task, and publication behaviors '
                        'discussed here; unexecuted examples remain explicitly labeled.',
             'sections': ['F-07']}],
 'architecture': [{'slug': 'models',
                   'title': 'Agents and resource models',
                   'purpose': 'An agent is an execution model, while an Agent Space or instance is a '
                              'product-specific configuration resource. The comparison starts with '
                              'these distinctions and then examines retained context.',
                   'sections': ['A-00', 'A-01', 'A-02']},
                  {'slug': 'boundaries',
                   'title': 'Integration and authorization boundaries',
                   'purpose': 'An integration connects a source, trigger, target, or destination. The '
                              'permitted direction and effect determine the relevant network and '
                              'authorization controls.',
                   'sections': ['A-08', 'A-03', 'A-04']},
                  {'slug': 'lifecycle',
                   'title': 'Execution lifecycles and evidence handoffs',
                   'purpose': 'A definition, execution, retained artifact, and external record have '
                              'separate lifecycles. Team handoffs preserve their identities rather than '
                              'collapsing them into one status.',
                   'sections': ['A-05', 'A-06']},
                  {'slug': 'example',
                   'title': 'Cross-platform worked example',
                   'purpose': 'The worked example assigns different questions to the three services '
                              'while retaining the source identity and verification responsibility for '
                              'each.',
                   'sections': ['A-U01']},
                  {'slug': 'evidence',
                   'title': 'Documentation coverage',
                   'purpose': 'These diagrams and comparisons are logical explanations of documented '
                              'behavior, not assertions about undisclosed runtime architecture.',
                   'sections': ['A-07']}]}
DECK_CHAPTERS={'devops': [('Service architecture', [0, 1]),
            ('Integrations and access', [2, 3, 4]),
            ('Knowledge and behavior', [5, 6, 7, 8]),
            ('Execution workflows', [9, 10, 11, 12, 13]),
            ('Operational use cases', [14, 15, 16]),
            ('Worked example', [17]),
            ('Troubleshooting and references', [18, 19, 20])],
 'security': [('Service architecture', [0, 1]),
              ('Integrations and access', [2, 3, 4, 5]),
              ('Knowledge and behavior', [6, 7, 8, 9]),
              ('Execution workflows', [10, 11, 12, 13, 14]),
              ('Operational use cases', [15, 16, 17, 18]),
              ('Worked example', [19]),
              ('Troubleshooting and references', [20])],
 'finops': [('Service architecture', [0, 1]),
            ('Integrations and access', [2, 3, 4, 5]),
            ('Knowledge and behavior', [6, 7]),
            ('Execution workflows', [8, 9, 10, 11, 12]),
            ('Operational use cases', [13, 14, 15]),
            ('Worked example', [16]),
            ('Troubleshooting and references', [17])],
 'architecture': [('Service architecture', [0, 1, 2]),
                  ('Integrations and access', [3, 4]),
                  ('Execution workflows', [5, 6, 7]),
                  ('Worked example', [8]),
                  ('Troubleshooting and references', [9, 10])]}
TYPES={'D-01': 'overview',
 'D-02': 'configuration',
 'D-03': 'configuration',
 'D-04': 'mechanism',
 'D-05': 'mechanism',
 'D-06': 'operation',
 'D-07': 'operation',
 'D-08': 'operation',
 'D-09': 'reference',
 'D-10': 'troubleshooting',
 'D-11': 'evidence',
 'S-01': 'overview',
 'S-02': 'configuration',
 'S-03': 'configuration',
 'S-04': 'operation',
 'S-05': 'operation',
 'S-06': 'operation',
 'S-07': 'troubleshooting',
 'S-08': 'evidence',
 'F-01': 'overview',
 'F-02': 'configuration',
 'F-03': 'operation',
 'F-04': 'operation',
 'F-05': 'configuration',
 'F-06': 'troubleshooting',
 'F-07': 'evidence',
 'A-01': 'overview',
 'A-02': 'mechanism',
 'A-03': 'mechanism',
 'A-04': 'mechanism',
 'A-05': 'operation',
 'A-06': 'operation',
 'A-07': 'evidence',
 'D-12': 'reference',
 'S-09': 'reference',
 'F-08': 'reference',
 'A-00': 'overview',
 'A-08': 'reference'}
LABELS={'overview': 'Overview and capabilities',
 'configuration': 'Configuration',
 'mechanism': 'Mechanism',
 'operation': 'Operation',
 'example': 'Worked example',
 'troubleshooting': 'Troubleshooting',
 'reference': 'Reference',
 'evidence': 'Official evidence'}
def section_type(sid):
    return "example" if "-U" in sid else "mechanism" if "-M" in sid else TYPES[sid]
