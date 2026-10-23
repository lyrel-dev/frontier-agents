---
id: settings-teaching-layout
kind: settings
data:
  boxes:
    request:
    - 15
    - 280
    - 205
    - 140
    instructions:
    - 270
    - 82
    - 260
    - 140
    skills:
    - 560
    - 82
    - 260
    - 140
    knowledge:
    - 850
    - 82
    - 260
    - 140
    execution:
    - 270
    - 270
    - 840
    - 140
    connections:
    - 470
    - 470
    - 350
    - 140
    learning:
    - 875
    - 470
    - 235
    - 140
    sources:
    - 470
    - 650
    - 350
    - 110
    result:
    - 1170
    - 280
    - 215
    - 140
    operator:
    - 15
    - 470
    - 205
    - 140
    destination:
    - 1170
    - 650
    - 215
    - 110
  products:
    devops:
      name: AWS DevOps Agent
      scope: Agent Space — access, definitions, context and execution records
      nodes:
        request:
        - external
        - Request / signal
        - Question, signal or trigger
        instructions:
        - aws
        - Instructions
        - Managed AGENTS.md or custom prompt
        skills:
        - aws
        - Skills
        - Applicable or assigned procedures
        knowledge:
        - aws
        - Memory stores
        - Available context; selected entries
        execution:
        - aws
        - Agent execution
        - A managed role or one custom-agent invocation
        connections:
        - aws
        - Integrations and tools
        - Provider association; selected operations
        learning:
        - aws
        - Knowledge production
        - Learning runs; feedback reflections
        sources:
        - external
        - Source systems
        - Resources, telemetry, code and deployment
        result:
        - aws
        - Result / record
        - Findings, plans, artifacts and history
        operator:
        - external
        - Operator
        - Scope, feedback, approval and review
        destination:
        - external
        - Destination
        - Configured channel or event consumer
      views:
        agent:
        - An agent uses guidance, procedures, context and authorized operations
        - - D-90
          - D-15
          - D-16
        - - request
          - instructions
          - skills
          - knowledge
          - execution
          - connections
          - sources
          - result
        coordination:
        - Managed responsibilities and knowledge reuse
        - - D-91
          - D-15
          - D-M08
        - - request
          - execution
          - knowledge
          - learning
          - result
          - connections
          - sources
        space:
        - The Agent Space contains configuration and execution context
        - - D-92
          - D-01
          - D-12
        - - request
          - instructions
          - skills
          - knowledge
          - execution
          - connections
          - learning
          - sources
          - result
          - operator
          - destination
        incident:
        - Incident triage and current-evidence investigation
        - - D-93
          - D-06
        - - request
          - execution
          - connections
          - sources
          - knowledge
          - result
        mitigation:
        - Mitigation planning and separately approved execution
        - - D-93
          - D-M06
        - - operator
          - execution
          - connections
          - sources
          - result
        learning:
        - Investigation history and correction become later context
        - - D-93
          - D-M01
          - D-M02
          - D-M08
        - - result
          - operator
          - learning
          - knowledge
          - execution
        reporting:
        - Service-health reporting reuses the same configured facilities
        - - D-93
          - D-16
          - D-19
        - - request
          - instructions
          - skills
          - execution
          - connections
          - sources
          - result
        knowledge:
        - Procedure maintenance and environment documentation
        - - D-93
          - D-M04
          - D-05
        - - operator
          - skills
          - sources
          - learning
          - knowledge
          - result
        change:
        - Configuration and release assurance use explicit subjects and effects
        - - D-93
          - D-22
        - - request
          - instructions
          - execution
          - connections
          - sources
          - operator
          - result
        review:
        - An operational review consumes independently verified outputs
        - - D-93
          - D-14
        - - result
          - operator
          - knowledge
    security:
      name: AWS Security Agent
      scope: Application Agent Space — settings, selected context and assessment records
      nodes:
        request:
        - external
        - Assessment request
        - Target, revision or document scope
        instructions:
        - aws
        - Assessment settings
        - Type, target rules and credentials
        skills:
        - aws
        - Selected criteria
        - Shared requirements used by eligible reviews
        knowledge:
        - aws
        - Application context
        - Selected source and application documents
        execution:
        - aws
        - Assessment execution
        - Assessment-specific run or one-off review
        connections:
        - aws
        - Source and target access
        - Repository, network path and test identity
        learning:
        - aws
        - Specific retained state
        - Login procedure; finding preferences
        sources:
        - external
        - Application and sources
        - Deployed target, code and documents
        result:
        - aws
        - Assessment result
        - Findings and verification evidence
        operator:
        - external
        - Application team
        - Authorize, review, deploy and accept
        destination:
        - external
        - Repository / Jira
        - Review or issue
      views:
        agent:
        - Security assessment inputs and execution
        - - S-90
          - S-12
        - - request
          - instructions
          - skills
          - knowledge
          - execution
          - connections
          - sources
          - result
        coordination:
        - Assessment, repair and verification are separate work records
        - - S-91
          - S-10
        - - request
          - execution
          - result
          - operator
          - connections
          - sources
        space:
        - Application scope and shared assessment criteria
        - - S-92
          - S-01
        - - request
          - instructions
          - skills
          - knowledge
          - execution
          - connections
          - learning
          - sources
          - result
          - operator
          - destination
        assessment:
        - Assess source or an authorized running application
        - - S-93
          - S-03
          - S-06
        - - request
          - instructions
          - knowledge
          - execution
          - connections
          - sources
          - result
        repair:
        - Finding triage, repair proposal, deployment and revalidation
        - - S-93
          - S-05
          - S-M05
        - - result
          - operator
          - execution
          - connections
          - sources
        context:
        - Criteria, application context and narrowly scoped reuse
        - - S-93
          - S-M03
          - S-M02
          - S-13
        - - skills
          - knowledge
          - learning
          - execution
          - result
    finops:
      name: AWS FinOps Agent
      scope: Agent instance — access, context, work records and destination connections
      nodes:
        request:
        - external
        - Question / trigger
        - Question, explicit task or automation
        instructions:
        - aws
        - Work instructions
        - Query basis and requested analysis
        skills:
        - aws
        - Context files
        - Mappings, instructions and report templates
        knowledge:
        - aws
        - Persistent memory
        - Preferences, corrections and task outcomes
        execution:
        - aws
        - Analysis execution
        - Direct conversation or an explicitly created queued task
        connections:
        - aws
        - Data and destination access
        - Source permissions; separate Jira / Slack binding
        learning:
        - aws
        - Context maintenance
        - Memory updates; separate compaction
        sources:
        - external
        - AWS data sources
        - Cost, anomaly and recommendation services
        result:
        - aws
        - Analysis result
        - Answer, artifact and task result
        operator:
        - external
        - Service owner
        - Reconcile, review publication and own changes
        destination:
        - external
        - Jira / Slack
        - Selected project or channel
      views:
        agent:
        - FinOps analysis combines source data and organizational context
        - - F-90
          - F-11
        - - request
          - instructions
          - skills
          - knowledge
          - execution
          - connections
          - sources
          - result
        coordination:
        - Requests and automations coordinate work through tasks
        - - F-91
          - F-03
        - - request
          - execution
          - connections
          - result
          - operator
        space:
        - Instance-scoped context, work and destinations
        - - F-92
          - F-01
          - F-09
        - - request
          - instructions
          - skills
          - knowledge
          - execution
          - connections
          - learning
          - sources
          - result
          - operator
          - destination
        analysis:
        - Historical cost and anomaly analysis retain source provenance
        - - F-93
          - F-M01
        - - request
          - instructions
          - execution
          - connections
          - sources
          - result
        reporting:
        - Periodic reporting adds a task definition and publication path
        - - F-93
          - F-03
          - F-04
          - F-M06
        - - request
          - instructions
          - skills
          - execution
          - connections
          - result
          - operator
          - destination
        optimization:
        - Recommendations are reviewed before engineering change and measurement
        - - F-93
          - F-14
        - - sources
          - connections
          - execution
          - result
          - operator
---

