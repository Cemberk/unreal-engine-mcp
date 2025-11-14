using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

# Button requiring 100 score
# Template: Conditional Button Device
# Button with conditions (score, items, team, etc.)

test_device_10 := class(creative_device):

    @editable
    ConditionalButton<private>: button_device = button_device{}

    @editable
    RequiredScore<private>:int = 100

    OnBegin<override>()<suspends>:void=
        ConditionalButton.InteractedWithEvent.Subscribe(OnButtonPressed)

    OnButtonPressed(Agent:agent):void=
        if (CheckConditions(Agent)):
            ExecuteButtonAction(Agent)
        else:
            Print("Conditions not met for {Agent}")

    CheckConditions(Agent:agent)<decides>:void=
        
    ExecuteButtonAction(Agent:agent):void=
        Print("Executing action for {Agent}")

    GetPlayerScore(Agent:agent):int=
        # Implement score retrieval
        return 0

    PlayerHasRequiredItem(Agent:agent)<decides>:void=
        # Implement item check
        false

    IsCorrectTeam(Agent:agent)<decides>:void=
        # Implement team check
        false