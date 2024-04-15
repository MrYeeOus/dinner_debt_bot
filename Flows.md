# Flows?
---
**/me**
    * Currently Owing:
    * Currently Owed:
    * Currently Earned:

**/owe**
    * Currently owe total:
        * Owe XYZ:
        * Owe ABC:
        * etc

---

**/spent**
    * $XX to be owed:
    * FORMAT:
        * /spent --> "How much?": ($$$) --> "Anyone excluded?": (@xyz, @abc, @etc) --> "For @xyz, how much is excluded?": ($$$)


---

JSON format:
{
    "ben": {
        "Earned": 0,
        "Owe":  {
            "chris": 0,
            "ed": 0
            "jacob": 0,
        }
    },
    "chris":    {
        "Earned": 0,
        "Owe":  {
            "ben": 0,
            "ed": 0
            "jacob": 0,
        }
    }
    "ed":    {
        "Earned": 0,
        "Owe":  {
            "ben": 0,
            "chris": 0
            "jacob": 0,
        }
    }
    "jacob":    {
        "Earned": 0,
        "Owe":  {
            "ben": 0,
            "chris": 0,
            "ed": 0
        }
    }
}
