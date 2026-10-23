"""Capability-oriented reading structure; frozen semantic records are unchanged."""
REVISION="2026-10-23-capability-exposition"
BASELINE="75f7d7c11d29e308e71a1bbe77ad93e9bc9f08a9"
CHAPTERS={'devops': [{'slug': 'workspace',
             'title': 'Workspace and resource organization',
             'purpose': 'Agent Spaces, AWS account connections, provider associations, and assets '
                        'establish the objects available for configuration.',
             'sections': ['D-01', 'D-13']},
            {'slug': 'definition',
             'title': 'Agent definition and customization',
             'purpose': 'Managed agents and custom-agent definitions expose different customization '
                        'controls. Invocation is covered separately.',
             'sections': ['D-15', 'D-16']},
            {'slug': 'knowledge',
             'title': 'Knowledge and behavioral context management',
             'purpose': 'Instructions, skills, memories, and attachments differ in purpose, production, '
                        'loading, and lifecycle.',
             'sections': ['D-M03', 'D-M04', 'D-M01', 'D-M08', 'D-M02', 'D-M07', 'D-17']},
            {'slug': 'invocation',
             'title': 'Invocation and triggers',
             'purpose': 'On-demand requests, schedules, and webhook events start work. Filtering '
                        'decides whether to start an invocation and what payload it receives.',
             'sections': ['D-07', 'D-18']},
            {'slug': 'integrations',
             'title': 'External system integrations',
             'purpose': 'Native providers, outbound MCP tools, and outbound A2A agents expose different '
                        'external operations.',
             'sections': ['D-12', 'D-03', 'D-20']},
            {'slug': 'network',
             'title': 'Network connectivity',
             'purpose': 'Private connections supply transport to endpoints; they are separate from '
                        'provider identity and tool authorization.',
             'sections': ['D-04']},
            {'slug': 'runtime',
             'title': 'Execution runtime and action control',
             'purpose': 'Invocations, continuation, Sandbox code execution, and directed actions have '
                        'different runtime and control boundaries.',
             'sections': ['D-19', 'D-M05', 'D-M06']},
            {'slug': 'managed-workflows',
             'title': 'Built-in managed workflows',
             'purpose': 'AWS-managed investigation, prevention, review, and release-assurance functions '
                        'apply the platform facilities to defined work.',
             'sections': ['D-06', 'D-21', 'D-22']},
            {'slug': 'interfaces',
             'title': 'Interaction surfaces, outputs, and outbound events',
             'purpose': 'Interfaces expose the service; artifacts and views represent its results; '
                        'lifecycle events notify external consumers.',
             'sections': ['D-09', 'D-05', 'D-23']},
            {'slug': 'administration',
             'title': 'Administration, security, and automation',
             'purpose': 'IAM and operator access, Asset APIs, infrastructure as code, credential '
                        'maintenance, and service telemetry support administration.',
             'sections': ['D-02', 'D-08', 'D-24', 'D-10']},
            {'slug': 'examples',
             'title': 'Worked example and reference material',
             'purpose': 'The approved operational objectives and prepared example remain separate from '
                        'the platform-capability explanation.',
             'sections': ['D-14', 'D-U01', 'D-11'],
             'appendix': True}],
 'security': [{'slug': 'workspace',
               'title': 'Workspace and resource organization',
               'purpose': 'Shared settings, application Agent Spaces, and assessment records have '
                          'distinct scopes.',
               'sections': ['S-01', 'S-10']},
              {'slug': 'definition',
               'title': 'Assessment definition and customization',
               'purpose': 'Assessment-specific settings select targets, sources, criteria, and effects; '
                          'they are not custom-agent definitions.',
               'sections': ['S-12']},
              {'slug': 'knowledge',
               'title': 'Application knowledge and assessment criteria',
               'purpose': 'Application context, requirements, retained login procedures, and finding '
                          'preferences have distinct producers and consumers.',
               'sections': ['S-M07', 'S-M03', 'S-M04', 'S-M02', 'S-13']},
              {'slug': 'invocation',
               'title': 'Assessment invocation',
               'purpose': 'Manual assessment requests, supported repository events, and pipeline '
                          'callers initiate the appropriate function.',
               'sections': ['S-14']},
              {'slug': 'integrations',
               'title': 'External system integrations',
               'purpose': 'Source-provider authorization, application-source selection, and publication '
                          'permissions are separate settings.',
               'sections': ['S-09']},
              {'slug': 'network',
               'title': 'Network connectivity',
               'purpose': 'Private source access and private application access are independent network '
                          'paths.',
               'sections': ['S-15']},
              {'slug': 'runtime',
               'title': 'Execution and assessment controls',
               'purpose': 'Target rules, credential resolution, and run state determine the scope and '
                          'conditions of a dynamic assessment.',
               'sections': ['S-03', 'S-M01', 'S-04']},
              {'slug': 'managed-workflows',
               'title': 'Managed assessment and remediation workflows',
               'purpose': 'Code/design review, threat modeling, finding handling, repair proposals, and '
                          'revalidation produce different records.',
               'sections': ['S-06', 'S-05', 'S-M05']},
              {'slug': 'interfaces',
               'title': 'Interaction surfaces and outputs',
               'purpose': 'Console administration, assessment workspaces, source comments, findings, '
                          'and external issues are distinct surfaces.',
               'sections': ['S-16']},
              {'slug': 'administration',
               'title': 'Administration, security, and limits',
               'purpose': 'User access, encryption identities, and execution limits require '
                          'product-specific configuration.',
               'sections': ['S-02', 'S-M06', 'S-07']},
              {'slug': 'examples',
               'title': 'Worked example and reference material',
               'purpose': 'Follow the approved finding workflow and inspect the prepared evidence '
                          'without changing the use-case catalog.',
               'sections': ['S-11', 'S-U01', 'S-08'],
               'appendix': True}],
 'finops': [{'slug': 'workspace',
             'title': 'Workspace and resource organization',
             'purpose': 'The agent instance, connections, conversations, automations, tasks, and '
                        'artifacts have different identities.',
             'sections': ['F-01', 'F-09']},
            {'slug': 'definition',
             'title': 'Instance configuration and task definition',
             'purpose': 'Instance settings control access and context; requests and automations define '
                        'the work.',
             'sections': ['F-11']},
            {'slug': 'knowledge',
             'title': 'Organizational knowledge and conversation context',
             'purpose': 'Uploaded files, retained preferences, and compaction are three different '
                        'context mechanisms.',
             'sections': ['F-M02', 'F-M03', 'F-M04']},
            {'slug': 'invocation',
             'title': 'Task invocation and automation',
             'purpose': 'Explicit requests, schedules, and supported anomaly events create work through '
                        'different start conditions.',
             'sections': ['F-03', 'F-M05']},
            {'slug': 'integrations',
             'title': 'Data-source and collaboration integrations',
             'purpose': 'AWS evidence sources and Jira/Slack destinations are configured for different '
                        'operations.',
             'sections': ['F-08', 'F-05']},
            {'slug': 'network',
             'title': 'Service access and data location',
             'purpose': 'Service interfaces, persistent storage location, and inference geography are '
                        'distinct properties.',
             'sections': ['F-12']},
            {'slug': 'runtime',
             'title': 'Execution runtime and publication control',
             'purpose': 'Task queueing and session execution precede destination-specific publication '
                        'controls.',
             'sections': ['F-13', 'F-M06']},
            {'slug': 'managed-workflows',
             'title': 'Managed analytical functions',
             'purpose': 'Historical analysis, forecasting, coverage, anomaly inquiry, and '
                        'recommendation analysis use different source results.',
             'sections': ['F-14', 'F-M01']},
            {'slug': 'interfaces',
             'title': 'Interaction surfaces and report artifacts',
             'purpose': 'Conversations, task history, report generation, and external publication '
                        'expose different outputs.',
             'sections': ['F-15', 'F-04']},
            {'slug': 'administration',
             'title': 'Administration, retention, and limits',
             'purpose': 'Role permissions, retained-data operations, and failure diagnosis must be '
                        'applied to the correct object.',
             'sections': ['F-02', 'F-M07', 'F-06']},
            {'slug': 'examples',
             'title': 'Worked example and reference material',
             'purpose': 'The approved reporting and investigation cases are illustrated with a '
                        'synthetic, reconcilable cost comparison.',
             'sections': ['F-10', 'F-U01', 'F-07'],
             'appendix': True}],
 'architecture': [{'slug': 'models',
                   'title': 'Concept ownership and product resource models',
                   'purpose': 'Use the entity model to distinguish responsibilities, then compare the '
                              'product capability dimensions. The model is not a product feature '
                              'inventory.',
                   'sections': ['A-00', 'A-10', 'A-12', 'A-11', 'A-09', 'A-01', 'A-02']},
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
DECK_CHAPTERS={'devops': [('Workspace and resource organization', [0, 1, 2]),
            ('Agent definition and customization', [3]),
            ('Knowledge and behavioral context management', [4, 5, 6, 7, 8]),
            ('Invocation and triggers', [9, 10]),
            ('External system integrations', [11, 12, 13, 14]),
            ('Network connectivity', [15]),
            ('Execution runtime and action control', [16, 17]),
            ('Built-in managed workflows', [18, 19, 20, 21]),
            ('Administration, security, and automation', [22, 23, 24]),
            ('Worked example and reference material', [25, 26, 27])],
 'security': [('Workspace and resource organization', [0, 1, 2, 3]),
              ('Assessment definition and customization', [4]),
              ('Application knowledge and assessment criteria', [5, 6, 7, 8]),
              ('External system integrations', [9, 10]),
              ('Network connectivity', [11]),
              ('Execution and assessment controls', [12, 13, 14]),
              ('Managed assessment and remediation workflows', [15, 16, 17]),
              ('Interaction surfaces and outputs', [18]),
              ('Administration, security, and limits', [19, 20, 21, 22]),
              ('Worked example and reference material', [23, 24])],
 'finops': [('Workspace and resource organization', [0, 1, 2]),
            ('Instance configuration and task definition', [3]),
            ('Organizational knowledge and conversation context', [4, 5]),
            ('Task invocation and automation', [6, 7, 8, 9]),
            ('Data-source and collaboration integrations', [10, 11, 12]),
            ('Service access and data location', [13]),
            ('Managed analytical functions', [14, 15, 16]),
            ('Interaction surfaces and report artifacts', [17, 18]),
            ('Administration, retention, and limits', [19, 20]),
            ('Worked example and reference material', [21, 22])],
 'architecture': [('Concept ownership and product resource models', [0, 1, 2, 3, 4, 5, 6]),
                  ('Integration and authorization boundaries', [7, 8, 9, 10]),
                  ('Execution lifecycles and evidence handoffs', [11, 12, 13]),
                  ('Cross-platform worked example', [14])]}
TYPES={'D-01': 'overview', 'D-02': 'configuration', 'D-03': 'configuration', 'D-04': 'mechanism', 'D-05': 'mechanism', 'D-06': 'operation', 'D-07': 'operation', 'D-08': 'operation', 'D-09': 'reference', 'D-10': 'troubleshooting', 'D-11': 'evidence', 'S-01': 'overview', 'S-02': 'configuration', 'S-03': 'configuration', 'S-04': 'operation', 'S-05': 'operation', 'S-06': 'operation', 'S-07': 'troubleshooting', 'S-08': 'evidence', 'F-01': 'overview', 'F-02': 'configuration', 'F-03': 'operation', 'F-04': 'operation', 'F-05': 'configuration', 'F-06': 'troubleshooting', 'F-07': 'evidence', 'A-01': 'overview', 'A-02': 'mechanism', 'A-03': 'mechanism', 'A-04': 'mechanism', 'A-05': 'operation', 'A-06': 'operation', 'A-07': 'evidence', 'D-12': 'reference', 'S-09': 'reference', 'F-08': 'reference', 'A-00': 'overview', 'A-08': 'reference', 'A-09': 'overview', 'D-13': 'reference', 'D-14': 'reference', 'S-10': 'reference', 'S-11': 'reference', 'F-09': 'reference', 'F-10': 'reference', 'A-10': 'overview', 'A-11': 'reference', 'D-15': 'reference', 'D-16': 'reference', 'D-M03': 'reference', 'D-M04': 'reference', 'D-M01': 'reference', 'D-M08': 'reference', 'D-M02': 'reference', 'D-17': 'reference', 'D-18': 'reference', 'D-20': 'reference', 'D-19': 'reference', 'D-21': 'reference', 'D-22': 'reference', 'D-23': 'reference', 'D-24': 'reference', 'S-12': 'reference', 'S-13': 'reference', 'S-14': 'reference', 'S-15': 'reference', 'S-16': 'reference', 'F-11': 'reference', 'F-12': 'reference', 'F-13': 'reference', 'F-14': 'reference', 'F-15': 'reference', 'A-12': 'reference'}
LABELS={'overview': 'Overview and capabilities', 'configuration': 'Configuration', 'mechanism': 'Mechanism', 'operation': 'Operation', 'example': 'Worked example', 'troubleshooting': 'Troubleshooting', 'reference': 'Reference', 'evidence': 'Official evidence'}
def section_type(sid):
    return "example" if "-U" in sid else TYPES.get(sid,"reference")
