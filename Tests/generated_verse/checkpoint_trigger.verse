using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

# Race checkpoint trigger
# Template: Trigger Volume Device
# Detects player entry/exit and triggers events

checkpoint_trigger := class(creative_device):

    @editable
    TriggerVolume<private>: trigger_device = trigger_device{}

    var PlayersInVolume<private>: [agent]logic = map{}

    OnBegin<override>()<suspends>:void=
        TriggerVolume.TriggeredEvent.Subscribe(OnPlayerEntered)

    OnPlayerEntered(Agent:?agent):void=
        if (PlayerAgent := Agent?):
            if (not PlayersInVolume[PlayerAgent]?):
                set PlayersInVolume[PlayerAgent] = true
                HandlePlayerEntry(PlayerAgent)

    OnPlayerExited(Agent:agent):void=
        if (set PlayersInVolume[Agent] = false):
            HandlePlayerExit(Agent)

    HandlePlayerEntry(Agent:agent):void=
        Print("{Agent} entered trigger volume")

    HandlePlayerExit(Agent:agent):void=
        Print("{Agent} exited trigger volume")

    GetPlayersInVolume():[]agent=
        var Players:[]agent = array{}
        for (KeyValue : PlayersInVolume):
            if (KeyValue(1)):
                set Players += array{KeyValue(0)}
        return Players