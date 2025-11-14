using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

# 60 second countdown timer
# Template: Timer Device Handler
# Supports countdown timers, interval timers, and repeating timers
# Generated: 2025-11-13 18:47:14

countdown_timer := class(creative_device):

    @editable
    GameTimer: timer_device = timer_device{}

    @editable
    TimerDuration<private>:float = 60.0

    @editable
    IsRepeating<private>:logic = false

    var IsTimerRunning<private>:logic = false

    # Called when the device is started in a running game
    OnBegin<override>()<suspends>:void=
        # Subscribe to timer events
        GameTimer.SuccessEvent.Subscribe(OnTimerComplete)
        GameTimer.CountdownEndEvent.Subscribe(OnCountdownEnd)

        Print("countdown_timer initialized - Duration: {TimerDuration}s")

    # Start the timer
    StartTimer():void=
        GameTimer.Start()
        set IsTimerRunning = true
        Print("Timer started")

    # Stop the timer
    StopTimer():void=
        GameTimer.Stop()
        set IsTimerRunning = false
        Print("Timer stopped")

    # Pause the timer
    PauseTimer():void=
        GameTimer.Pause()
        Print("Timer paused")

    # Resume the timer
    ResumeTimer():void=
        GameTimer.Resume()
        Print("Timer resumed")

    # Reset the timer
    ResetTimer():void=
        GameTimer.Reset()
        set IsTimerRunning = false
        Print("Timer reset")

    # Handles timer completion
    OnTimerComplete():void=
        Print("Timer completed")
        set IsTimerRunning = false

        if (IsRepeating):
            # Restart timer if repeating
            StartTimer()

    # Handles countdown end event
    OnCountdownEnd():void=
        Print("Countdown ended")

    # Get timer progress (0.0 to 1.0)
    GetTimerProgress():float=
        # Return progress percentage
        # CurrentTime := GameTimer.GetCurrentTime()
        # return CurrentTime / TimerDuration
        return 0.0