This repository shows a cryptographic way to validate user phone number in registration flow.

Here is the sequence diagram for this flow:

![sequence diagram](/sequence-diagram.png)

For more details read [this]().

### Example:

```python
from main import PhoneVerification

# Get verification code
phone_verification = PhoneVerification(secret_key='VEcGULCPPAuAaD7QtcMd')
state, verification_code = phone_verification.generate_verification_state(phone_number='+12025550331')
print('This is state: ', state)
print('This is verification code: ', verification_code)

# Validate verification code
validation_result = phone_verification.validate_state(state, verification_code)
print('This is validation result: ', validation_result)
```

And this is the output:

```commandline
This is state:  State(timestamp=1673730351.149517, digest='4b68d6f3c5d9f21037ee8f1649e93a8274408026df356387c0d1d286f46e9304', phone_number='+12025550331')
This is verification code:  89402
This is validation result:  True
```