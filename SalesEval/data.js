const projectData = {
    ka: {
        name: "Green Canyon",
        location: "წალკა, საქართველო (1500მ სიმაღლეზე)",
        roi: "8-12% წლიური",
        capitalAppreciation: "20-30% მშენებლობის დასრულებამდე",
        prices: {
            studio: "$59,500-დან",
            oneBed: "$85,000-დან",
            cottages: "$150,000-დან $440,000-მდე"
        },
        paymentTerms: {
            downpayment: "15-30%",
            installments: "36 თვიანი 0% განვადება",
            escrow: "საერთაშორისო Escrow ანგარიშები (ბანკის გარანტია)"
        },
        timeline: {
            start: "2026 წლის ზაფხული",
            completion: "2030 წლის გაზაფხული (36 თვე)"
        },
        features: ["LEED/Green Globe სერთიფიკატი", "Radisson Standard MEP", "Smart Home", "სპა, რესტორანი, ზიპ-ლაინი"],
        objections: {
            price: "თქვენ ყიდულობთ 5-ვარსკვლავიან ეკოსისტემას და ტერნქეი რემონტს (Bosch/Grohe).",
            climate: "გრილი ზაფხული (20-22°C) - საუკეთესო თავშესაფარი სიცხისგან.",
            trust: "Escrow ანგარიში - დეველოპერი ფულს იღებს მხოლოდ ეტაპების ჩაბარების შემდეგ."
        }
    },
    en: {
        name: "Green Canyon",
        location: "Tsalka, Georgia (1500m altitude)",
        roi: "8-12% Annual",
        capitalAppreciation: "20-30% before completion",
        prices: {
            studio: "From $59,500",
            oneBed: "From $85,000",
            cottages: "From $150,000 to $440,000"
        },
        paymentTerms: {
            downpayment: "15-30%",
            installments: "36-month 0% installments",
            escrow: "International Escrow accounts (Bank guarantee)"
        },
        timeline: {
            start: "Summer 2026",
            completion: "Spring 2030 (36 months)"
        },
        features: ["LEED/Green Globe Certification", "Radisson Standard MEP", "Smart Home", "Spa, Restaurant, Zip-line"],
        objections: {
            price: "You are purchasing a 5-star ecosystem with turnkey renovation (Bosch/Grohe).",
            climate: "Cool summer (20-22°C) - the best escape from heat.",
            trust: "Escrow account - direct developer payment only after stage completion."
        }
    }
};

const personas = [
    {
        id: "investor",
        name: { ka: "ბატონი ხანი", en: "Mr. Khan" },
        description: { ka: "ინვესტორი დუბაიდან, აინტერესებს ROI და უსაფრთხოება.", en: "Investor from Dubai, interested in ROI and safety." },
        initialMessage: { ka: "გამარჯობა, მაინტერესებს თქვენი პროექტი. რა გარანტიები მაქვს და რა იქნება ჩემი წლიური მოგება?", en: "Hello, I'm interested in your project. What guarantees do I have and what will be my annual return?" },
        traits: ["skeptical", "logical", "safety-first"]
    },
    {
        id: "wellness",
        name: { ka: "თამარი", en: "Tamar" },
        description: { ka: "ადგილობრივი მაცხოვრებელი, ეძებს აგარაკს ოჯახისთვის.", en: "Local resident, looking for a cottage for her family." },
        initialMessage: { ka: "გამარჯობა, წალკა ძალიან ცივი ხომ არ არის? და რითია თქვენი კოტეჯები გამორჩეული?", en: "Hello, isn't Tsalka too cold? And what makes your cottages special?" },
        traits: ["lifestyle-oriented", "nature-lover"]
    }
];

export { projectData, personas };
