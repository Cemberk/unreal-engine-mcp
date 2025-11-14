using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

# Tracks coin collection progress
# Template: Collectible Manager
# Manages collectible items (coins, tokens, etc.)

coin_collector := class(creative_device):

    @editable
    Collectibles<private>: []item_spawner_device = array{}

    var CollectedCount<private>: [agent]int = map{}
    var TotalCollectibles<private>:int = 0

    OnBegin<override>()<suspends>:void=
        set TotalCollectibles = Collectibles.Length

        for (Collectible : Collectibles):
            Collectible.ItemPickedUpEvent.Subscribe(OnCollectiblePickedUp)

    OnCollectiblePickedUp(Agent:agent):void=
        CurrentCount := if (Count := CollectedCount[Agent]?) then Count else 0
        set CollectedCount[Agent] = CurrentCount + 1

        Print("{Agent} collected item ({CurrentCount + 1}/{TotalCollectibles})")

        if (CurrentCount + 1 >= TotalCollectibles):
            OnAllCollected(Agent)

    OnAllCollected(Agent:agent):void=
        Print("{Agent} collected all items!")

    GetCollectibleCount(Agent:agent):int=
        if (Count := CollectedCount[Agent]?):
            return Count
        return 0

    ResetCollectibles():void=
        set CollectedCount = map{}
        for (Collectible : Collectibles):
            Collectible.Enable()