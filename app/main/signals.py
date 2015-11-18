from blinker import Namespace

# Signal namespace setup
main_signals = Namespace()

# Create signals
email_address_changed = main_signals.signal('email-address-changed')
