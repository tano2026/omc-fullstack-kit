# Galileo/Travelport Ticketing Guidelines & Commission (BSP/LCC/NDC) Links

When dealing with Galileo GDS (1G) ticket issuance, refund, reissue, and commission (com) rate lookups for airlines in Vietnam, use these direct, authoritative links instead of searching from scratch.

## 1. Key Official Resource Links (Galileo Vietnam)
*   **Galileo Remind Me Portal (Main):** `https://galileo.vn/remindme/`
    *   *Structure:* Legacy HTML Frameset. Main Left TOC tree resides at `https://galileo.vn/remindme/webhelpcontents.htm`.
*   **BSP Airline Issuance & Commission Policies (Vietnam):** `https://1gindo.com/bsp/index.htm`
    *   *Details:* Contains comprehensive matrix of BSP airlines (e.g., 3U, 7C, 8M, AC, AE, etc.), including automatic ticketing codes (Z-rates/com percentage like Z3, Z5), Revalidation/Reissue rules, Refund criteria, Void codes, and EasyPay status. This is updated regularly (e.g., UPDATE 22MAY26).
*   **LCC Airline Ticketing Manual:** `https://1gindo.com/lcc/`
*   **NDC Booking Manual (Singapore Airlines SQ, Air France AF, etc.):** `https://1gindo.com/ndcs/index.htm`
*   **Airline Contact Directory:** `https://1gindo.com/remindme/AirlineContact/index.htm`

## 2. Galileo/Amadeus Passport (APIS / DOCS) Formats
*   **Amadeus (Standard Format from User):**
    ```text
    SR DOCS YY HK1-P-VNM-[Passport_No]-VNM-[DOB_DDMMMYY]-[Gender_M_or_F]-[Expiry_DDMMMYY]-[Surname]/[First_&_Middle_Names]
    ```
    *   *Example:* `SR DOCS YY HK1-P-VNM-Q00762070-VNM-24NOV81-F-05JAN36-NGUYEN/DINH VY ANH`
*   **Send Passport Info to ALL Airlines in Galileo (YY):**
    ```text
    SI.P{Pax_No}/SSRDOCSYYHK1/P/{Issuing_Country}/{Passport_No}/{Nationality}/{DOB_DDMMMYY}/{Gender}/{Expiry_DDMMMYY}/{Surname}/{First_&_Middle_Names}
    ```
    *   *Example:* `SI.P1/SSRDOCSYYHK1/P/VN/Q00762070/VN/24NOV81/F/05JAN36/NGUYEN/DINH VY ANH`
*   **Send to a Specific Airline (e.g., Vietnam Airlines - VN):**
    ```text
    SI.P{Pax_No}/SSRDOCSVNHK1/P/{Issuing_Country}/{Passport_No}/{Nationality}/{DOB_DDMMMYY}/{Gender}/{Expiry_DDMMMYY}/{Surname}/{First_&_Middle_Names}
    ```
    *   *Example:* `SI.P1/SSRDOCSVNHK1/P/VN/Q00762070/VN/24NOV81/F/05JAN36/NGUYEN/DINH VY ANH`
*   **Infant Format (INFT) - use 'FI' or 'MI' for gender:**
    ```text
    SI.P{Pax_No}/SSRDOCSYYHK1/P/{Issuing_Country}/{Passport_No}/{Nationality}/{DOB_DDMMMYY}/{Gender_FI_or_MI}/{Expiry_DDMMMYY}/{Surname}/{First_&_Middle_Names}
    ```
    *   *Example:* `SI.P4/SSRDOCSYYHK1/P/VN/Q00762070/VN/24NOV81/FI/05JAN36/NGUYEN/DINH VY ANH`
