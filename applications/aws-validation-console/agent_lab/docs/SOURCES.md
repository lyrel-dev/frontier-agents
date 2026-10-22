# Primary contracts reviewed

Reviewed 22 October 2026. These references define the external APIs, not proof that this installation has successfully exercised them. SDK Stubber contract tests used boto3/botocore 1.43.18; live requests and account-specific permissions remain to be accepted.

- AWS DevOps Agent CreateBacklogTask: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateBacklogTask.html
- Optional reference object requirements: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ReferenceInput.html
- ListBacklogTasks: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListBacklogTasks.html
- Journal records: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html
- ListRecommendations: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListRecommendations.html
- Version-pinned GetRecommendation: https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetRecommendation.html
- Cross-account configuration: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-multiple-aws-accounts.html
- IAM action/resource contract: https://docs.aws.amazon.com/service-authorization/latest/reference/list_devops-agent.html
- Lifecycle-event timing: https://docs.aws.amazon.com/devopsagent/latest/userguide/integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-devops-agent-events-detail-reference.html
- FIS StartExperiment/idempotency: https://docs.aws.amazon.com/fis/latest/APIReference/API_StartExperiment.html
- FIS action contract: https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html
- FIS stop conditions: https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html
- FIS safety lever: https://docs.aws.amazon.com/fis/latest/userguide/safety-lever.html
- SSM Automation execution: https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_StartAutomationExecution.html
- Automation tags for reconciliation: https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_ListTagsForResource.html

A request-contract review corrected an invalid partial optional task reference in the working code. Internal assisted/evaluation requests now omit that optional object; native trials observe the actual reference supplied by the existing incident integration. No invented association ID or URL is inserted to make a request validate.
