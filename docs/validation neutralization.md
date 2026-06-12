1. Neutralized Normalization & Validation
  As requested, I have made the normalization and validation functions more lenient to prevent them from breaking the
  authentication flow. They now log warnings instead of raising exceptions.

   * core/validators.py:
       * prefix validator: No longer raises ValueError for incorrect formats; it logs a warning and returns the input
         value.
       * validate_link & validate_username: No longer raise ValueError on regex mismatch; they log a warning and
         return the input value.
   * core/normalise.py:
       * normalise_link: No longer raises ValueError if URL parsing fails; it logs a warning and returns the original
         string.

  2. Identified & Fixed Errors in Auth Flow

   * Typo in Password Verification: Fixed a typo in services/security/helper.py where utf=8 was used instead of utf-8
     in the verify_password function.
   * Redundant Session Closing: Removed session.close() from AuthService.register and AuthService.login. Since the
     database session is managed by FastAPI's get_db dependency, closing it manually in the service was redundant and
     could lead to errors if the route or dependency teardown attempted to access it afterward.
   * Profile Deletion Logic: In repo/profile.py, fixed delete_profile which:
       * Failed to handle the PW prefix for PetOwnerProfile (it only checked for OWN).
       * Could raise an UnboundLocalError if an unrecognized prefix was passed.
       * Now supports FAC, CLN, PHM, OWN, and PW prefixes.

  3. Other Observations

   * Registration vs. Profile: The current AuthService.register only creates a User record. It does not create the
     corresponding entry in the specific profile tables (e.g., pet_owner_profile). This means the delete_user route
     might attempt to delete a profile that doesn't exist yet (though I've added safety checks to prevent this from
     crashing).
   * Update Schema: The /user/update route requires the full createUser schema, meaning users must provide and confirm
     their password even for simple name updates.
   * JWT Role Consistency: Verified that the role "fac" is consistently used in both registration and login for
     facilitators.

  The authentication flow is now more robust against validation failures and includes fixes for critical bugs like the
  password encoding typo.
