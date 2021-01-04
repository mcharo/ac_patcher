# ac_patcher

AnyConnect Route Table Patch for macOS (adapted from [Garrett Skjelstad's code](https://github.com/garrettskj/ac_patcher))

## How it works

The AnyConnect macOS Binary uses the following C++ method: `CHostConfigMgr::StartInterfaceAndRouteMonitoring()`

The following python script finds that method, then backtracks to where that method is being called from, and then NOPs out that call.

Since each version of AnyConnect this memory address will change, I needed something that would do this process automatically, hence the scripting of radare2.

## How to use it

1. Install AnyConnect
2. Install dependencies:

    ```bash
    brew install radare2
    python -m pip install r2pipe
    ```

## Run the patcher

This will stop the system service, disassemble the binary looking for the methods, and patch it out and then restart the service.

You'll need to `sudo` this for elevated privileges, because the default installation directory `/opt/cisco/anyconnect/` requires elevated privileges for writing

```bash
sudo ./anyconnect_patcher.py -f /opt/cisco/anyconnect/bin/vpnagentd
```

## Version Compatibility

Tested / Confirmed with:

- 4.7.00136 (macOS Catalina 10.15.5)
