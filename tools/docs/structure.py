"""Maintained chapter membership and presentation grouping."""
REVISION="2026-10-23-technical-editorial-review"
BASELINE='75f7d7c11d29e308e71a1bbe77ad93e9bc9f08a9'
CHAPTERS={'devops': [{'slug': 'model',
             'title': 'Resource model and scope',
             'purpose': 'Begin with the product-specific entities, their scope and their relationships. '
                        'Configuration, executions, knowledge and external evidence are distinct '
                        'objects with different lifecycles.',
             'sections': ['D-01', 'D-13']},
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
             'title': 'Applying the model to operational outcomes',
             'purpose': 'Trace the approved use cases through their concrete configuration and '
                        'execution objects, then examine the prepared evidence. The examples remain '
                        'synthetic, not live AWS results.',
             'sections': ['D-14', 'D-U01']},
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
               'title': 'Resource model and scope',
               'purpose': 'Begin with the product-specific entities, their scope and their '
                          'relationships. Configuration, executions, knowledge and external evidence '
                          'are distinct objects with different lifecycles.',
               'sections': ['S-01', 'S-10']},
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
               'title': 'Applying the model to operational outcomes',
               'purpose': 'Trace the approved use cases through their concrete configuration and '
                          'execution objects, then examine the prepared evidence. The examples remain '
                          'synthetic, not live AWS results.',
               'sections': ['S-11', 'S-U01']},
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
             'title': 'Resource model and scope',
             'purpose': 'Begin with the product-specific entities, their scope and their relationships. '
                        'Configuration, executions, knowledge and external evidence are distinct '
                        'objects with different lifecycles.',
             'sections': ['F-01', 'F-09']},
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
             'title': 'Applying the model to operational outcomes',
             'purpose': 'Trace the approved use cases through their concrete configuration and '
                        'execution objects, then examine the prepared evidence. The examples remain '
                        'synthetic, not live AWS results.',
             'sections': ['F-10', 'F-U01']},
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
                   'title': 'Concept ownership and product resource models',
                   'purpose': 'Read the approved conceptual model, its ownership notation and each '
                              'product specialization before comparing knowledge or execution behavior.',
                   'sections': ['A-00', 'A-10', 'A-11', 'A-09', 'A-01', 'A-02']},
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
DECK_CHAPTERS={'devops': [('Product-specific resource model', [0, 1, 2]),
            ('Integrations and access', [3, 4, 5]),
            ('Knowledge and behavior', [6, 7, 8]),
            ('Incident response and operational execution', [9, 10, 11, 12, 13, 14, 15]),
            ('Operational objectives and implementation', [16, 17, 18, 19, 20]),
            ('Worked example', [21]),
            ('Troubleshooting and references', [22])],
 'security': [('Product-specific resource model', [0, 1, 2]),
              ('Integrations and access', [3, 4, 5, 6]),
              ('Knowledge and behavior', [7, 8, 9, 10]),
              ('Execution workflows', [11, 12, 13, 14, 15]),
              ('Operational objectives and implementation', [16, 17, 18, 19]),
              ('Worked example', [20]),
              ('Troubleshooting and references', [21])],
 'finops': [('Product-specific resource model', [0, 1, 2]),
            ('Integrations and access', [3, 4, 5, 6]),
            ('Knowledge and behavior', [7, 8]),
            ('Execution workflows', [9, 10, 11, 12, 13]),
            ('Operational objectives and implementation', [14, 15, 16, 17]),
            ('Worked example', [18]),
            ('Troubleshooting and references', [19])],
 'architecture': [('Concept model and product specialization', [0, 1, 2, 3]),
                  ('Outcome and implementation relationships', [4, 5, 6]),
                  ('Integrations and access', [7, 8]),
                  ('Execution workflows', [9, 10, 11]),
                  ('Worked example', [12]),
                  ('Troubleshooting and references', [13, 14])]}
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
 'A-08': 'reference',
 'A-09': 'overview',
 'D-13': 'reference',
 'D-14': 'reference',
 'S-10': 'reference',
 'S-11': 'reference',
 'F-09': 'reference',
 'F-10': 'reference',
 'A-10': 'overview',
 'A-11': 'reference'}
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
