using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

# Button with 5 second cooldown
# Template: Button Device Handler
# Generated: 2025-11-13 18:47:14

cooldown_button := class(creative_device):

    @editable
    CooldownButton: button_device = button_device{}

    # Called when the device is started in a running game
    OnBegin<override>()<suspends>:void=
        # Subscribe to button interaction events
        CooldownButton.InteractedWithEvent.Subscribe(OnButtonPressed)

        Print("cooldown_button initialized")

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