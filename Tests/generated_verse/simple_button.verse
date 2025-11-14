using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

# Simple button press handler
# Template: Button Device Handler
# Generated: 2025-11-13 18:47:14

simple_button := class(creative_device):

    @editable
    ActionButton: button_device = button_device{}

    # Called when the device is started in a running game
    OnBegin<override>()<suspends>:void=
        # Subscribe to button interaction events
        ActionButton.InteractedWithEvent.Subscribe(OnButtonPressed)

        Print("simple_button initialized")

    # Handles button press events
    OnButtonPressed(Agent:agent):void=
        Print("{Agent} pressed the button")

        # Example: Trigger additional logic
        # PerformAction(Agent)

    # Helper: Get team ID for agent
    GetTeamID(Agent:agent):int=
        if (FortChar := Agent.GetFortCharacter[], Team := FortChar.GetTeam[]):
            return Team.GetTeamIndex()
        return -1