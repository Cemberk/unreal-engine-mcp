using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }
using { /UnrealEngine.com/Temporary/Diagnostics }

# 10 second repeating timer
# Template: Timer Device Handler
# Supports countdown timers, interval timers, and repeating timers
# Generated: 2025-11-13 18:47:14

interval_timer := class(creative_device):

    @editable
    IntervalTimer: timer_device = timer_device{}

    @editable
    TimerDuration<private>:float = 10.0

    @editable
    IsRepeating<private>:logic = true

    var IsTimerRunning<private>:logic = false

    # Called when the device is started in a running game
    OnBegin<override>()<suspends>:void=
        # Subscribe to timer events
        IntervalTimer.SuccessEvent.Subscribe(OnTimerComplete)
        IntervalTimer.CountdownEndEvent.Subscribe(OnCountdownEnd)

        Print("interval_timer initialized - Duration: {TimerDuration}s")

    # Start the timer
    StartTimer():void=
        IntervalTimer.Start()
        set IsTimerRunning = true
        Print("Timer started")

    # Stop the timer
    StopTimer():void=
        IntervalTimer.Stop()
        set IsTimerRunning = false
        Print("Timer stopped")

    # Pause the timer
    PauseTimer():void=
        IntervalTimer.Pause()
        Print("Timer paused")

    # Resume the timer
    ResumeTimer():void=
        IntervalTimer.Resume()
        Print("Timer resumed")

    # Reset the timer
    ResetTimer():void=
        IntervalTimer.Reset()
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
        # CurrentTime := IntervalTimer.GetCurrentTime()
        # return CurrentTime / TimerDuration
        return 0.0