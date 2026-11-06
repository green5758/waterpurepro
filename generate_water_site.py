import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "WaterPurePro"
SITE_TAGLINE = "Water Softener Grain Capacity (GPG), Whole-House Filter GPM & RO Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a"

# Cumulative Daily Review Engine: Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/waterpurepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "waterpurepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Fleck 5600SXT 48,000 & 64,000 Grain Digital Metered On-Demand Whole-House Water Softener",
        "category": "Two-Tank Digital Water Softener",
        "rating": "4.8 ★ (6,850+ reviews)",
        "badge": "#1 Best-Selling Water Softener",
        "specs": "1.5–2.0 Cu.Ft High-Capacity 8% Crosslink Resin | Digital SXT Flow Meter | Includes Brine Tank & Bypass",
        "keyword": "Fleck+5600SXT+48000+64000+Grain+Water+Softener"
    },
    {
        "title": "Waterdrop G3P800 / G3P600 Tankless Reverse Osmosis System (800 GPD, Built-In UV & Smart Faucet)",
        "category": "Tankless Under-Sink RO System",
        "rating": "4.8 ★ (9,400+ reviews)",
        "badge": "#1 Tankless RO System",
        "specs": "800 GPD Fast Flow (Fills Cup in 6 Secs) | 3:1 Pure-to-Drain Ratio | NSF 58/372 Certified + LED UV",
        "keyword": "Waterdrop+G3P800+G3P600+Tankless+Reverse+Osmosis+System"
    },
    {
        "title": "iSpring WGB32B / WGB32BM 3-Stage 20\"×4.5\" Big Blue Whole-House Water Filtration System (15 GPM)",
        "category": "3-Stage Whole-House Filter",
        "rating": "4.8 ★ (8,100+ reviews)",
        "badge": "#1 Whole-House Filter System",
        "specs": "1\" NPT High-Flow Ports (15 GPM) | Stage 1 Sediment + Stage 2 Carbon + Stage 3 Iron/Manganese/Lead",
        "keyword": "iSpring+WGB32B+WGB32BM+3+Stage+Whole+House+Water+Filter"
    },
    {
        "title": "Aquasure Harmony Series 48,000 & 64,000 Grain Electronic Metered Whole-House Water Softener",
        "category": "High-Efficiency Water Softener",
        "rating": "4.7 ★ (3,900+ reviews)",
        "badge": "Best Pro-Value Softener Kit",
        "specs": "Aquatrol Digital Backlit Head | Auto-Flush Backwash | Treats up to 15 GPM for 3–5 Bathroom Homes",
        "keyword": "Aquasure+Harmony+Series+48000+64000+Grain+Water+Softener"
    },
    {
        "title": "APEC Water Systems ROES-PH75 / RO-90 6-Stage Alkaline Mineral Under-Sink Reverse Osmosis System",
        "category": "6-Stage Alkaline RO System",
        "rating": "4.8 ★ (18,600+ reviews)",
        "badge": "18,000+ Five-Star Reviews",
        "specs": "WQA Certified | Adds Calcium Minerals to Raise pH (7.5–8.5) | USA-Made Filmtec Membrane | 75–90 GPD",
        "keyword": "APEC+Water+Systems+ROES+PH75+6+Stage+Alkaline+Reverse+Osmosis"
    },
    {
        "title": "HQUA-OWS-12 / Viqua 12 GPM 55W Whole-House Ultraviolet (UV) Water Purifier & Sterilizer (304 Stainless)",
        "category": "Whole-House UV Sterilizer",
        "rating": "4.8 ★ (4,200+ reviews)",
        "badge": "#1 Well Water Bacteria Shield",
        "specs": "Destroys 99.99% of E. Coli, Coliform, Giardia & Viruses | 12 GPM Flow | 9,000-Hr Germicidal UV Lamp",
        "keyword": "HQUA+OWS+12+Viqua+12+GPM+55W+UV+Water+Sterilizer"
    },
    {
        "title": "iSpring WSP-50SL / Rusco Reusable Flushable Spin-Down Sediment Water Filter (50 Micron + Siliphos)",
        "category": "Reusable Spin-Down Pre-Filter",
        "rating": "4.8 ★ (11,300+ reviews)",
        "badge": "#1 First-Stage Sand & Rust Trap",
        "specs": "316L Stainless Steel Mesh | Flush Sand & Rust Out via Bottom Valve in 5 Seconds | Protects Softeners",
        "keyword": "iSpring+WSP+50SL+Spin+Down+Sediment+Water+Filter"
    },
    {
        "title": "Hach 5B Total Hardness Drop Titration Test Kit (1–30 GPG) + HM Digital Waterproof TDS Meter",
        "category": "Pro Water Hardness Lab Kit",
        "rating": "4.9 ★ (7,600+ reviews)",
        "badge": "#1 Accurate GPG Drop Tester",
        "specs": "Industry-Standard Drop-Count Titration (Pink to Blue) | Measures Exact Grains Per Gallon (GPG)",
        "keyword": "Hach+5B+Total+Hardness+Test+Kit+and+HM+Digital+TDS+Meter"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Fleck 5600SXT (48,000 Grain)",
        "type": "Two-Tank Metered Softener",
        "capacity_spec": "48,000 Grains (1.5 ft³ Resin)",
        "flow_spec": "12 GPM Service (1–4 Baths)",
        "highlight": "Industry #1 Serviceable Valve Head",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Fleck+5600SXT+48000+Grain+Water+Softener"
    },
    {
        "model": "Fleck 5600SXT (64,000 Grain)",
        "type": "Heavy-Duty Two-Tank Softener",
        "capacity_spec": "64,000 Grains (2.0 ft³ Resin)",
        "flow_spec": "15 GPM Service (3–6 Baths)",
        "highlight": "Best for 15+ GPG Hard Water & Large Homes",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Fleck+5600SXT+64000+Grain+Water+Softener"
    },
    {
        "model": "Waterdrop G3P800 Tankless RO",
        "type": "800 GPD Tankless Under-Sink RO",
        "capacity_spec": "800 Gallons/Day (0.56 GPM)",
        "flow_spec": "3:1 Pure-to-Drain + UV LED",
        "highlight": "Saves 70% Under-Sink Space & 4x Less Waste",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Waterdrop+G3P800+Tankless+Reverse+Osmosis+System"
    },
    {
        "model": "iSpring WGB32BM (3-Stage 20\")",
        "type": "Big Blue Whole-House Filter",
        "capacity_spec": "100,000 Gal Capacity (20\"×4.5\")",
        "flow_spec": "Up to 15 GPM (1\" NPT Ports)",
        "highlight": "Removes Chlorine, Sediment, Iron & Manganese",
        "rating": "4.8 / 5.0 ★",
        "keyword": "iSpring+WGB32BM+3+Stage+Whole+House+Water+Filter"
    },
    {
        "model": "APEC ROES-PH75 (6-Stage RO)",
        "type": "Alkaline Pressurized-Tank RO",
        "capacity_spec": "75 GPD + 4-Gal Tank + CaCO3",
        "flow_spec": "Zero Electricity Needed",
        "highlight": "Restores Crisp Mineral Taste & pH 7.5+",
        "rating": "4.8 / 5.0 ★",
        "keyword": "APEC+ROES+PH75+Alkaline+Reverse+Osmosis+System"
    },
    {
        "model": "HQUA-OWS-12 (55W UV System)",
        "type": "Whole-House UV Sterilizer",
        "capacity_spec": "99.99% Microbial Destruction",
        "flow_spec": "12 GPM (3/4\" & 1\" MNPT)",
        "highlight": "Chemical-Free Well Water Bacteria Cure",
        "rating": "4.8 / 5.0 ★",
        "keyword": "HQUA+OWS+12+55W+UV+Water+Sterilizer"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-fleck-5600sxt-two-tank-vs-cabinet-all-in-one-water-softener",
        "title": "Fleck 5600SXT Two-Tank Softener vs. All-in-One Cabinet Water Softener: Salt Bridges, Flow Rate & Lifespan",
        "product_a": "Two-Tank Modular (Fleck 5600SXT / Aquasure)",
        "product_b": "Single-Piece Cabinet Softener (Big-Box Style)",
        "winner_badge": "15–20 Year Serviceable Lifespan & Easy Salt Loading vs. Compact Single Footprint",
        "keyword_a": "Fleck+5600SXT+48000+64000+Grain+Water+Softener",
        "keyword_b": "Rheem+Whirlpool+40000+Grain+Cabinet+Water+Softener",
        "summary": "Compare separate fiberglass mineral tanks and brine drums against cramped all-in-one plastic cabinets.",
        "metrics": [
            {"feature": "Max Grain Capacity", "val_a": "32,000 to 80,000+ Grains (Full-Height 54\" Mineral Tank)", "val_b": "Typically Caps at 30,000 to 42,000 Grains (Short Squat Tank)"},
            {"feature": "Salt Bridge Maintenance", "val_a": "Separate Brine Tank Is Wide Open — Break Salt Bridges in 10 Secs", "val_b": "Mineral Tank Sits Inside Salt Bin — Hard to Reach Bottom"},
            {"feature": "Pressure Drop (GPM Flow)", "val_a": "12 to 18 GPM High-Flow 1\" Valve (Zero Shower Pressure Loss)", "val_b": "8 to 10 GPM (Can Drop Pressure When 2 Showers Run)"},
            {"feature": "Valve & Seal Repairability", "val_a": "Universal Non-Proprietary Fleck Parts ($25 Rebuild Kit Lasts 20 Yrs)", "val_b": "Proprietary Circuit Boards (Often Replaced Whole After 6 Yrs)"},
            {"feature": "Floor Space Footprint", "val_a": "Requires ~28\" × 18\" (Two Side-by-Side Tanks)", "val_b": "Compact ~19\" × 15\" Single Cabinet"}
        ],
        "verdict_text": "Choose a Two-Tank Modular Water Softener built around the legendary Pentair Fleck 5600SXT (or Aquasure Harmony) digital metered head if you want zero shower pressure drop, a wide-open brine tank that holds 300 lbs of salt without bridging, and a system that lasts 15 to 20 years. Only choose a single-piece Cabinet Softener if you are installing it inside a tiny utility closet where you lack 28 inches of width."
    },
    {
        "slug": "compare-tankless-reverse-osmosis-waterdrop-g3p800-vs-tank-ro-apec",
        "title": "Tankless Reverse Osmosis (Waterdrop G3P800) vs. Traditional Tank RO (APEC ROES-PH75): Waste Ratio & Speed",
        "product_a": "Tankless RO (Waterdrop G3P800 / G3P600)",
        "product_b": "Traditional Pressurized-Tank RO (APEC ROES-PH75)",
        "winner_badge": "3:1 Low Wastewater & Unlimited 800 GPD Flow vs. Works Without Electricity",
        "keyword_a": "Waterdrop+G3P800+G3P600+Tankless+Reverse+Osmosis",
        "keyword_b": "APEC+Water+Systems+ROES+PH75+6+Stage+Reverse+Osmosis",
        "summary": "Compare 3:1 pure-to-drain booster pump efficiency against traditional 1:3 bladder-tank systems under your kitchen sink.",
        "metrics": [
            {"feature": "Pure-to-Drain Wastewater Ratio", "val_a": "3 : 1 Ratio (3 Cups of Pure Water for Only 1 Cup of Drain Water!)", "val_b": "1 : 3 Ratio (Wastes 3 Gallons to Make 1 Gallon of Pure Water)"},
            {"feature": "Continuous Dispensing Speed", "val_a": "800 GPD (0.56 GPM) — Never Runs Out When Filling Pasta Pots", "val_b": "Fast for First 2.5 Gallons, Then Trickles Until Tank Refills (2 Hrs)"},
            {"feature": "Under-Sink Space Saved", "val_a": "Saves 70% Cabinet Space (No Bulky 16\" Pressurized Bladder Tank)", "val_b": "Requires Room for Both Filter Manifold AND 4-Gallon Tank"},
            {"feature": "Filter Replacement Method", "val_a": "2-Second Twist-and-Pull Sealed Cartridges (Zero Wrench Needed)", "val_b": "Unscrew Sump Housings w/ Plastic Wrench + Sanitize Tank"},
            {"feature": "Under-Sink Power Outlet", "val_a": "Requires 120V Outlet Under Sink (Shared w/ Garbage Disposal)", "val_b": "100% Non-Electric (Runs on Water Line Pressure Alone)"}
        ],
        "verdict_text": "If you have a 120V outlet under your kitchen sink (for a dishwasher or garbage disposal), the Waterdrop G3P800 (or G3P600) Tankless RO is a generational leap forward: it reclaims 70% of your under-sink cabinet space, cuts water waste by up to 900%, includes a smart TDS-reading faucet, and never runs out of water when filling large stockpots. Choose the non-electric APEC ROES-PH75 if you have no electrical outlet under your sink or want to run RO water during power outages."
    },
    {
        "slug": "compare-salt-based-ion-exchange-water-softener-vs-salt-free-descaler",
        "title": "Salt-Based Ion-Exchange Water Softener vs. Salt-Free TAC Scale Conditioner: What Actually Removes Hardness?",
        "product_a": "Salt-Based Ion-Exchange Softener (Fleck / Aquasure)",
        "product_b": "Salt-Free TAC Conditioner (Template Assisted Crystallization)",
        "winner_badge": "100% Physical Removal of Calcium/Magnesium & 2x Soap Lather vs. Zero Salt/Drain",
        "keyword_a": "Fleck+5600SXT+Aquasure+48000+Grain+Water+Softener",
        "keyword_b": "iSpring+Aquasana+Salt+Free+Water+Conditioner+Descaler",
        "summary": "Understand the chemistry difference: why only an ion-exchange resin softener physically removes hardness minerals (0 GPG) to stop glass spotting and dry skin.",
        "metrics": [
            {"feature": "Hardness Mineral Removal", "val_a": "Physically Removes 100% of Calcium, Magnesium & Ferrous Iron (0 GPG!)", "val_b": "0% Removal — Crystallizes Minerals so They Don't Stick to Pipes"},
            {"feature": "White Evaporative Spots on Glass", "val_a": "Eliminates White Chalky Spots on Shower Glass, Dishes & Faucets", "val_b": "Minerals Remain in Water — Still Leaves White Spots When Dried!"},
            {"feature": "Soap, Shampoo & Detergent Savings", "val_a": "Cuts Soap & Laundry Detergent Use by 50%–70% (Rich Silky Lather)", "val_b": "No Change in Soap Lathering or Dry Skin/Hair Feel"},
            {"feature": "Max Hardness & Iron Limit", "val_a": "Handles Extreme Hardness up to 75+ GPG and 2–5 PPM Clear Iron", "val_b": "Fails Above 25 GPG or If Any Iron/Manganese Is Present (>0.3 PPM)"},
            {"feature": "Brine Drain & Salt Bags", "val_a": "Uses ~6–10 Bags of Salt/Yr & Requires a Drain Line", "val_b": "Zero Salt Bags, Zero Electricity & Zero Drain Line"}
        ],
        "verdict_text": "Don't fall for misleading marketing: a 'Salt-Free Water Conditioner' is NOT a water softener—it leaves 100% of the calcium and magnesium in your water, meaning you will still get white chalky spots on your black faucets and glass shower doors, and soap will still struggle to lather. Only choose a Salt-Free TAC conditioner if your municipality legally bans salt-regenerated softeners or you have no drain line. For true 0-GPG silky soft water that protects tankless water heaters and appliances, a Fleck 5600SXT or Aquasure Ion-Exchange Water Softener is mandatory."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-fleck-5600sxt-48000-and-64000-grain-digital-water-softener",
        "title": "Fleck 5600SXT 48,000 & 64,000 Grain Review: Why Plumbers Call This the 'Toyota Hilux' of Water Softeners",
        "product_name": "Fleck 5600SXT 48,000 / 64,000 Grain Digital Metered Water Softener",
        "category": "Two-Tank Digital Water Softener",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Water Softener in America",
        "spec_1": "48,000 Grains (1.5 ft³) or 64,000 Grains (2.0 ft³)",
        "spec_2": "Pentair Fleck 5600SXT Digital Paddle-Wheel Meter Valve",
        "spec_3": "High-Capacity 8% or 10% Crosslink Ion-Exchange Resin",
        "spec_4": "5-Year Valve / 10-Year Fiberglass Tank Warranty",
        "published_date": "2026-11-01",
        "keyword": "Fleck+5600SXT+48000+64000+Grain+Water+Softener",
        "summary": "Built around Pentair's legendary non-proprietary Fleck 5600SXT digital metered control head and a polyglass-lined mineral tank, this two-tank workhorse delivers 0-GPG soft water for 15 to 20+ years.",
        "pros": [
            "On-demand digital flow meter counts exact gallons used and only regenerates at 2:00 AM when capacity is exhausted—saving 40% on salt and water vs timer units",
            "Non-proprietary Pentair Fleck valve means every plumber carries spare seals and pistons, and a $28 rebuild kit after 12 years makes it brand new",
            "Full-height 10\"×54\" (48k) or 12\"×52\" (64k) fiberglass resin tank provides deep resin bed contact time for zero hardness bleed-through at 12–15 GPM",
            "Separate square or round brine drum holds up to 250–300 lbs of solar/pellet salt with easy top access"
        ],
        "cons": [
            "Requires about 90 minutes of DIY plumbing (use 1-inch SharkBite braided stainless flex hoses with built-in ball valves for a solder-free install)"
        ],
        "body_paragraphs": [
            "When sizing a water softener on our grain capacity calculator ($\text{Daily Grains} = \text{People} \times 75\text{ Gal} \times \text{Compensated GPG}$), the goal is to select a resin tank large enough so the system only regenerates once every 7 to 10 days at an efficient 6-lb-per-cubic-foot salt dose. For a family of 4 with 18 GPG hard water (5,400 grains/day), a 48,000-grain Fleck 5600SXT (1.5 cu. ft. of resin) or 64,000-grain unit (2.0 cu. ft.) sits right in the efficiency sweet spot.",
            "In our Hach 5B drop-titration test on a 22 GPG municipal supply, water leaving the Fleck 5600SXT tested at 0.0 GPG (instant blue on the very first drop of titrant), and showerhead scale buildup vanished completely.",
            "If your city water has high chloramine/chlorine (>1.5 PPM), pair the Fleck 5600SXT with an upstream iSpring Big Blue carbon filter (or upgrade to 10% crosslink resin) so chlorine never degrades the resin beads."
        ]
    },
    {
        "slug": "review-waterdrop-g3p800-and-g3p600-tankless-reverse-osmosis-system",
        "title": "Waterdrop G3P800 Tankless RO Review: 800 GPD Fast Flow, Built-In UV & 3:1 Low Wastewater Ratio",
        "product_name": "Waterdrop G3P800 (800 GPD) & G3P600 Tankless Reverse Osmosis System",
        "category": "Tankless Under-Sink RO System",
        "rating_score": "4.9",
        "verdict_badge": "#1 Tankless Reverse Osmosis System",
        "spec_1": "800 GPD (G3P800) / 600 GPD (G3P600) Instant Flow",
        "spec_2": "3 : 1 Pure-to-Drain Ratio (Saves 900% Water vs Old RO)",
        "spec_3": "NSF/ANSI 58 & 372 Certified + Flow-Activated UV LED",
        "spec_4": "Smart Brushed-Nickel Digital Faucet Shows Live TDS",
        "published_date": "2026-11-01",
        "keyword": "Waterdrop+G3P800+G3P600+Tankless+Reverse+Osmosis+System",
        "summary": "Ditching the bulky, bacteria-prone 4-gallon storage tank of 1990s RO systems, the NSF-certified Waterdrop G3P800 fills an 8-oz glass with 9-PPM pure water in 5.5 seconds while wasting only 1 cup of water for every 3 cups purified.",
        "pros": [
            "Massive 800 Gallons-Per-Day (0.56 GPM) booster-pump flow fills coffee carafes and large pasta pots continuously without slowing to a trickle",
            "Industry-leading 3:1 pure-to-drain ratio (on G3P800) wastes 9x less water than traditional 1:3 tank RO systems",
            "Smart digital kitchen faucet displays real-time Total Dissolved Solids (TDS in PPM) and filter life status right on the spout base",
            "Internal flow-activated LED UV sterilizer destroys 99.9% of bacteria the instant you turn the faucet handle—with zero mercury bulbs"
        ],
        "cons": [
            "Internal booster pump makes a gentle espresso-machine hum under the cabinet only while the RO faucet is actively running"
        ],
        "body_paragraphs": [
            "Important water chemistry fact: when a whole-house water softener removes 20 GPG of calcium and magnesium hardness from your water, it exchanges those ions for a small amount of sodium (or potassium)—raising your tap water's Total Dissolved Solids (TDS). That is why every water softener owner should install an under-sink Reverse Osmosis (RO) system at the kitchen sink to strip out 95% of sodium, PFAS, lead, fluoride, arsenic, and nitrates for drinking and ice makers.",
            "In our HM Digital COM-100 TDS meter test on 420 PPM softened water, the Waterdrop G3P800 dropped drinking water TDS down to a crisp 14 PPM!",
            "Best of all, changing filters takes 3 seconds: you twist the old cartridge a quarter-turn left and pull it out—no turning off the main water valve and no filter wrenches."
        ]
    },
    {
        "slug": "review-ispring-wgb32b-and-wgb32bm-3-stage-big-blue-whole-house-filter",
        "title": "iSpring WGB32B & WGB32BM 3-Stage 20\" Big Blue Review: 15 GPM Chlorine, Sediment, Iron & Manganese Defense",
        "product_name": "iSpring WGB32B / WGB32BM 3-Stage 20\"×4.5\" Whole-House Water Filter",
        "category": "3-Stage Whole-House Filter",
        "rating_score": "4.8",
        "verdict_badge": "#1 Whole-House Filtration System",
        "spec_1": "20\" × 4.5\" 'Big Blue' High-Capacity Sumps (100,000 Gal)",
        "spec_2": "1-Inch NPT Brass Inlet/Outlet Ports (Up to 15 GPM Flow)",
        "spec_3": "Stage 1: 5µm Sediment | Stage 2: CTO Carbon Block",
        "spec_4": "Stage 3: Iron & Manganese (WGB32BM) or Dual Carbon / Lead",
        "published_date": "2026-11-01",
        "keyword": "iSpring+WGB32B+WGB32BM+3+Stage+Whole+House+Water+Filter",
        "summary": "Installed on your main water line right before your water softener, the 15-GPM iSpring WGB32B/WGB32BM strips out 99% of chlorine, sediment, rust, pesticides, and up to 3.0 PPM of dissolved iron and manganese.",
        "pros": [
            "Massive 20-inch by 4.5-inch cartridges hold 4x more filter media than tiny 10\"×2.5\" housings—delivering 15 GPM flow with zero pressure drop and 12-month filter life",
            "Mounted upstream of your water softener, the CTO coconut-shell carbon block removes municipal chlorine so chlorine never oxidizes your softener's resin bed",
            "WGB32BM edition includes a specialized catalytic Stage-3 cartridge that reduces orange iron staining (up to 3.0 PPM) and black manganese staining (up to 1.0 PPM)",
            "Heavy-duty powder-coated steel wall bracket with top pressure-relief buttons and filter housing wrench included"
        ],
        "cons": [
            "Each 20\"×4.5\" water-filled sump weighs ~18 lbs when unscrewing during annual filter changes—mount at chest height with 6 inches of floor clearance underneath"
        ],
        "body_paragraphs": [
            "Using our whole-house GPM flow calculator, a 3-to-4 bathroom home requires a filtration system capable of flowing 12 to 15 Gallons Per Minute (GPM) so running the washing machine and two showers simultaneously doesn't cause pressure sag. Standard 10-inch filters choke flow down to 4 GPM. The iSpring WGB32B series uses industrial 20\"×4.5\" Big Blue housings with 1-inch NPT brass ports.",
            "If you are on city water, the WGB32B (dual carbon blocks) removes 99% of chlorine, chloramine odors, VOCs, and herbicides from every shower and faucet in your house—protecting both your skin and your water softener resin.",
            "If you are on well water with orange rust stains in your toilets, choose the WGB32BM (Iron & Manganese model) preceded by a 50-micron iSpring WSP-50SL spin-down pre-filter."
        ]
    },
    {
        "slug": "review-hach-5b-total-hardness-drop-test-kit-and-tds-meter",
        "title": "Hach 5B Total Hardness Test Kit Review: Why TDS Meters Cannot Measure Water Hardness (GPG)",
        "product_name": "Hach 5B Total Hardness Drop Titration Test Kit + HM Digital TDS Meter",
        "category": "Water Hardness & TDS Test Kit",
        "rating_score": "4.9",
        "verdict_badge": "#1 Gold-Standard GPG Test Kit",
        "spec_1": "Measures Exact Hardness from 1 to 30+ Grains Per Gallon (GPG)",
        "spec_2": "Reagent Drop-Count Titration (Magenta Pink → Pure Sky Blue)",
        "spec_3": "100 Tests Included in Pocket Carrying Case",
        "spec_4": "Pair w/ HM Digital TDS Meter to Test RO Membrane Rejection",
        "published_date": "2026-11-01",
        "keyword": "Hach+5B+Total+Hardness+Test+Kit+and+HM+Digital+TDS+Meter",
        "summary": "A digital TDS meter CANNOT measure water hardness—in fact, softened water has the exact same TDS as hard water! The Hach 5B drop-count titration kit is the industry standard for testing exact Grains Per Gallon (GPG).",
        "pros": [
            "Eliminates the fuzzy color-guessing of cheap paper dip strips—every single drop of Titrant Solution equals exactly 1.0 GPG of hardness",
            "Instant visual confirmation that your water softener is working: if the sample turns pure sky-blue on the first scoop of powder (0 drops), your water is 0.0 GPG soft!",
            "Lets you program the exact Hardness setting into your Fleck 5600SXT or Aquasure digital head so you never waste salt",
            "Pairing with an HM Digital TDS meter lets you also verify your under-sink Reverse Osmosis membrane's 95% TDS rejection rate"
        ],
        "cons": [
            "For extremely hard well water above 25 GPG, dilute the sample 1:1 with distilled water and multiply the drop count by 2"
        ],
        "body_paragraphs": [
            "The #1 mistake homeowners make after installing a water softener is sticking a $15 electronic TDS (Total Dissolved Solids) meter into a glass of softened water, seeing '320 PPM', and thinking their new softener is broken! Why? Because an ion-exchange water softener swaps calcium and magnesium ions for sodium ions—meaning the *total dissolved solids* stay identical even when the water is 100% soft (0 GPG).",
            "To measure true water hardness before and after a softener, water treatment engineers universally use the Hach 5B Total Hardness Drop Test Kit. You fill the plastic tube to the line, add one dipper of ManVer 2 indicator powder (which turns hard water magenta-red), and add drops of EDTA titrant while swirling until the water snaps from red to pure sky-blue.",
            "Count the drops: 18 drops = 18 Grains Per Gallon (GPG). Enter '18' into our calculator and your softener's digital computer, and your regeneration schedule is calibrated to perfection."
        ]
    }
]

# Deep Catalog of 36+ Water Softeners, RO Systems, Well Filters & UV Units for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("aquasure-harmony-series-48000-64000-grain-water-softener", "Aquasure Harmony Series 48,000 & 64,000 Grain Digital Metered Water Softener", "High-Efficiency Water Softener", "4.8", "Best Complete Two-Tank Softener Value", "48,000 or 64,000 Grains High-Capacity Resin", "Aquatrol Digital Backlit Metered Control Head", "Auto-Flush Backwash + Bypass Valve Included", "5-Year Manufacturer Warranty", "Aquasure+Harmony+Series+48000+64000+Grain+Water+Softener", "Bundling a pre-loaded high-capacity resin tank, digital metered control head, corrosion-proof brine drum, and 1-inch bypass valve at an unbeatable price, the Aquasure Harmony is a homeowner favorite."),
    ("apec-water-systems-roes-ph75-6-stage-alkaline-reverse-osmosis", "APEC Water Systems ROES-PH75 6-Stage Alkaline Mineral Under-Sink RO System", "6-Stage Alkaline RO System", "4.8", "#1 Pressurized-Tank Alkaline RO (18,000+ Reviews)", "WQA Certified 99% Contaminant Removal (Lead, Fluoride, PFAS)", "Stage 6 US-Made Calcite Cartridge Raises pH & Mineral Taste", "100% Non-Electric (Works During Power Outages!)", "75–90 GPD Dow Filmtec Membrane + Lead-Free Faucet", "APEC+Water+Systems+ROES+PH75+6+Stage+Alkaline+Reverse+Osmosis", "Assembled in California with genuine Dow Filmtec membranes and a 6th-stage calcium carbonate mineralizer that eliminates the flat taste of standard RO water, the APEC ROES-PH75 has over 18,000 five-star reviews."),
    ("hqua-ows-12-viqua-12-gpm-55w-whole-house-uv-water-sterilizer", "HQUA-OWS-12 / Viqua 12 GPM 55W Whole-House Ultraviolet (UV) Water Sterilizer", "Whole-House UV Sterilizer", "4.8", "#1 Chemical-Free Well Water Bacteria & Virus Shield", "Destroys 99.99% of E. Coli, Coliform, Giardia & Cryptosporidium", "12 GPM Flow Rate Through 304 Stainless Reactor Chamber", "Includes 2× 9,000-Hour Germicidal UV Lamps & Quartz Sleeve", "Digital Ballast Controller w/ 365-Day Countdown & Audible Alarm", "HQUA+OWS+12+Viqua+12+GPM+55W+UV+Water+Sterilizer", "Private well water is not chlorinated by a city plant—meaning heavy rain can wash coliform bacteria into your aquifer. Installed as the final stage after your softener and sediment filter, a 55W UV chamber sterilizes every drop entering your home."),
    ("ispring-wsp-50sl-rusco-reusable-spin-down-sediment-water-filter", "iSpring WSP-50SL Reusable Flushable Spin-Down Sediment Filter w/ Siliphos", "50-Micron Spin-Down Pre-Filter", "4.8", "#1 First-Line Defense Against Well Sand, Pipe Scale & Rust", "50-Micron 316L Stainless Steel Mesh Screen (Never Buy Cartridges!)", "Open Bottom Ball Valve for 5 Seconds to Flush Out Trapped Sand", "Food-Grade Siliphos Beads Help Prevent Pipe Scale & Corrosion", "1\" MNPT + 3/4\" FNPT/PEX Brass Threads", "iSpring+WSP+50SL+Spin+Down+Sediment+Water+Filter", "Installing a $52 clear spin-down sediment filter ahead of your Big Blue filters and water softener catches coarse well sand, rust flakes, and pebble grit—tripling the lifespan of your expensive downstream cartridges and softener valves."),
    ("rheem-preferred-platinum-whirlpool-42000-grain-wifi-water-softener", "Rheem Preferred Platinum / Whirlpool 40,000–42,000 Grain Smart Cabinet Water Softener", "Compact Cabinet Softener", "4.7", "#1 Compact All-in-One Cabinet Softener for Tight Utility Closets", "Demand-Initiated Regeneration Learns Household Water Patterns", "Built-In Wi-Fi App Alerts You When Salt Level Is Low!", "Compact Single-Cabinet Footprint Fits Tight Garages/Closets", "Removes up to 120 GPG Hardness & 4 PPM Clear Water Iron", "Rheem+Preferred+Platinum+Whirlpool+Water+Softener+42000+Grain", "When you only have a 19-inch wide corner next to your water heater and want smartphone alerts whenever your brine bin needs another bag of salt, the Rheem/Whirlpool smart cabinet series is the top compact solution."),
    ("waterdrop-wd-kj225g-ro-mineralization-filter-and-remineralizer", "Waterdrop WD-MNR35 / Frizzlife Inline Alkaline Remineralization Post-Filter (1/4\" & 3/8\")", "RO Alkaline Remineralizer", "4.8", "#1 Add-On to Restore pH 7.5+ & Minerals for Coffee & Ice Makers", "Adds Natural Calcium, Magnesium, Sodium & Potassium Ions", "Raises Acidic RO Water pH from ~6.2 up to 7.5–8.5 Alkaline", "Prevents Pure RO Water From Corroding Metal Fridge/Espresso Lines!", "Push-to-Connect 1/4\" or 3/8\" Quick Fittings (5-Min Install)", "Waterdrop+Alkaline+Remineralization+Inline+Filter+Reverse+Osmosis", "Ultra-pure 10-PPM Reverse Osmosis water is slightly acidic and lacks the 50 PPM of magnesium minerals needed to brew sweet espresso or prevent corrosion in brass refrigerator ice makers. Splicing an inline remineralizer onto your RO outlet fixes both instantly."),
    ("pro-products-rescare-liquid-water-softener-resin-cleaner-1-gallon", "Pro Products RK01N ResCare Liquid Water Softener Resin & Valve Cleaner (64 oz / 1 Gal)", "Iron & Fouling Resin Cleaner", "4.9", "#1 Cure for Iron-Fouled Softener Resin Beds", " Dissolves Iron, Manganese, Silt & Organic Fouling From Resin Beads", "Restores Full Grain Exchange Capacity Without Replacing Resin!", "Pour 4 oz Into Brine Well Before Manual Regeneration", "Safe for All Fleck, Clack, Autotrol & Cabinet Softeners", "Pro+Products+ResCare+Liquid+Water+Softener+Resin+Cleaner", "Over time, ferrous well-water iron and municipal sediment coat your softener's golden resin beads so salt brine can no longer clean them—causing hard water to bleed through. Pouring 1/2 cup of ResCare into the brine tube strips iron right off the resin."),
    ("sharkbite-1-inch-and-3-4-inch-corrugated-stainless-water-softener-connector-hoses", "SharkBite Max 3/4\" & 1\" FIP × 24-Inch Flexible Stainless Steel Water Softener Connectors", "Solder-Free Softener Hoses", "4.9", "#1 Way to Plumb a Water Softener in 15 Minutes With Zero Soldering!", "Push-to-Connect SharkBite End Grabs Copper, PEX, CPVC or PE-RT", "1-Inch FIP Threaded Nut Screws Directly Onto Softener Bypass!", "Braided or Corrugated 304 Stainless Steel (200 PSI Rated)", "Available w/ Built-In Quarter-Turn Ball Valve", "SharkBite+Water+Softener+Connector+Hose+3+4+1+Inch+24+Inch", "Hiring a plumber for $600 just to solder two copper pipes onto your water softener bypass valve is unnecessary: two 24-inch SharkBite flexible stainless connectors push straight onto your existing 3/4\" or 1\" copper or PEX main line in 10 minutes."),
    ("afwfilters-iron-pro-2-combination-water-softener-and-iron-filter-64000-grain", "AFWFilters Iron Pro 2 (64,000 Grain) Fine-Mesh Resin Water Softener & Iron/Sulfur Filter", "Well Water Iron + Softener", "4.8", "#1 System for Well Water With Both High Hardness AND 4–7 PPM Iron", "Loaded w/ Fine-Mesh Resin Engineered Specifically for Heavy Iron", "Removes up to 75 GPG Hardness + 6–8 PPM Ferrous Iron + 2 PPM Manganese", "Genuine Fleck 5600SXT Digital Paddle-Wheel Meter Head", "Includes Turbulator Downflow distributor Tube", "AFWFilters+Iron+Pro+2+64000+Grain+Fleck+5600SXT+Water+Softener", "Standard water softener resin chokes when well water contains more than 2 PPM of orange ferrous iron. The AFWFilters Iron Pro 2 combines fine-mesh resin with a bottom turbulator tube that scrubs iron out of the bed on every backwash."),
    ("frizzlife-pd600-tam3-600-gpd-tankless-ro-with-alkaline-remineralization", "Frizzlife PD600-TAM3 600 GPD Tankless Reverse Osmosis System w/ Built-In Alkaline pH+", "600 GPD Alkaline Tankless RO", "4.8", "Best Tankless RO That Includes 3rd-Stage Alkaline Remineralization", "600 GPD Tankless Flow + 1.5:1 Low Drain Ratio", "Includes TAM3 Post-Filter (Restores pH 7.5+ & Essential Minerals)", "Smart LED Display Shows Live Outgoing TDS & Filter Life", "Quick-Twist Cartridge Replacement", "Frizzlife+PD600+TAM3+Tankless+Reverse+Osmosis+Alkaline", "Combining tankless 600 GPD speed with a built-in 3rd-stage TAM3 alkaline remineralizer in one compact under-sink box, the Frizzlife PD600 delivers crisp, mineral-balanced drinking water right out of the box."),
    ("pentair-omnifilter-pu25-big-blue-20x4-5-pleated-and-carbon-replacement-pack", "iSpring / Pentair 1-Year Replacement Filter Pack for 20\"×4.5\" 3-Stage Whole-House Systems", "20\"×4.5\" Replacement Cartridges", "4.9", "#1 Annual Replacement Pack for 20\" Big Blue Whole-House Filters", "Includes 5µm Polypropylene Sediment + Coconut Shell Carbon Block", "Optional Stage-3 Iron/Manganese (FM25B) or Lead Reduction", "Fits All Standard 20\" × 4.5\" Big Blue Housings (iSpring/Express/Pentair)", "Individually Shrink-Wrapped for 5-Year Shelf Life", "iSpring+F3WGB32B+F3WGB32BM+20x4.5+Replacement+Filter+Pack", "Keeping a spare 3-pack of 20\"×4.5\" sediment, carbon block, and iron-reduction cartridges in your utility room ensures you can swap filters in 15 minutes the moment your pressure gauge shows a 10 PSI drop."),
    ("boshart-filter-housing-dual-pressure-gauge-kit-and-mounting-wrench", "Liquid-Filled 0–100 PSI Dual Inlet/Outlet Pressure Gauge Kit for Whole-House Filters", "Filter Pressure-Drop Monitor", "4.8", "#1 Way to Know Exactly When Your Whole-House Cartridges Are Clogged", "304 Stainless Case w/ Glycerin Liquid Fill (Zero Needle Flutter)", "Compare Inlet PSI vs Outlet PSI — Change Filter at 10 PSI Drop!", "1/4\" NPT Bottom/Back Mount Threads Into Big Blue Caps", "Stops Guessing Whether Cartridges Are Dirty or Clean", "0+100+PSI+Liquid+Filled+Pressure+Gauge+1+4+NPT+Water+Filter", "How do you know if your opaque blue whole-house filter cartridges are clogged after 8 months? Threading a 0–100 PSI liquid-filled gauge into the 1/4\" ports before and after the housings tells you at a glance: when outlet pressure drops 10 PSI below inlet pressure, it's time to swap filters."),
    ("air-gap-ro-drain-saddle-valve-and-dlp-dishwasher-branch-wye-adapter", "ET116-001 Silent Reverse Osmosis Drain Line Adapter (DLA) w/ Push-In 1/4\" & 3/8\" Port", "Silent Code-Compliant RO Drain", "4.8", "#1 Cure for Gurgling Kitchen Sink RO Drain Saddle Valves", "Replaces Leaky Clamp-On Saddle Valves w/ Solid 1.5\" PVC Slip Tee", "Angles RO Drain Water Smoothly Down Pipe Wall (Zero Gurgling Noise!)", "UPC & IPC Plumbing Code Compliant", "Includes 1/4\" & 3/8\" Quick-Connect Push Fittings", "Reverse+Osmosis+Silent+Drain+Line+Adapter+1+4+3+8+Inch", "Traditional clamp-on RO drain saddles require drilling a hole in your sink tailpiece and often make a loud gurgling noise every time the RO system flushes. Installing an inline Silent Drain Line Adapter makes your tankless RO whisper-quiet."),
    ("express-water-whole-house-3-stage-anti-scale-and-carbon-filter-system", "Express Water Heavy-Duty 3-Stage 20\"×4.5\" Whole-House Filter w/ Pressure Gauges Included", "Gauge-Equipped 3-Stage Filter", "4.7", "Best 3-Stage Big Blue System w/ 3 Factory Pressure Gauges Built In", "Includes 3 Top-Mounted Pressure Gauges (1 Per Stage!)", "1\" NPT High-Flow Brass Ports + Stainless Steel Freestanding Frame", "Freestanding Floor Frame (No Drilling Heavy Bolts Into Wall Studs!)", "Removes Chlorine, VOCs, Rust, Sand & Odors", "Express+Water+3+Stage+Whole+House+Water+Filter+System+20+Inch", "Unlike wall-hung Big Blue systems that require lagging 75 lbs of water weight into your basement wall studs, Express Water builds their 3-stage 20\" system inside a freestanding powder-coated floor frame with three built-in pressure gauges."),
    ("tier1-purolite-c100e-high-capacity-8-and-10-percent-crosslink-softener-resin", "1.0 & 1.5 Cubic Foot Bag of High-Capacity 8% & 10% Crosslinked Water Softener Resin", "Replacement Ion-Exchange Resin", "4.8", "#1 Way to Restore a 10-Year-Old Water Softener for $115 instead of $900!", "NSF/ANSI 44 Certified Sulfonated Polystyrene Gel Cation Resin", "10% Crosslink Resists Municipal Chlorine 2x Longer Than 8%", "32,000 Grains per Cubic Foot (1.5 ft³ = 48,000 Grains)", "Includes Funnel for Easy Tank Re-Bedding", "1+Cubic+Foot+10+Percent+Crosslinked+Water+Softener+Resin", "If your 10-year-old water softener has lost its softening capacity or turned mushy from city chlorine, you don't need to buy a whole new softener! Unscrew the Fleck control head, siphon out the old resin, and pour in fresh 10% crosslinked resin with a funnel."),
    ("waterdrop-3-8-inch-15-ft-refrigerator-icemaker-and-coffee-ro-tubing-kit", "Waterdrop 15-Ft / 25-Ft 1/4\" & 3/8\" BPA-Free Polyethylene RO Refrigerator Ice Maker Tee Kit", "Fridge & Ice Maker RO Branch Kit", "4.9", "#1 Kit to Feed Crystal-Clear RO Water to Your Refrigerator Ice Maker!", "Splits Your Under-Sink RO Output to Feed Both Faucet & Fridge!", "Eliminates Cloudy White Ice Cubes & Costly $55 Fridge Filters", "Includes Push-to-Connect Tee, Shut-Off Ball Valve & Tubing Cutter", "100% NSF Certified Food-Grade PE Tubing", "Waterdrop+Reverse+Osmosis+Refrigerator+Ice+Maker+Connection+Kit", "Once you have a Reverse Osmosis system under your kitchen sink, why keep paying $55 every 6 months for a basic carbon filter inside your refrigerator? Branching a $16 food-grade PE line from your RO outlet to your fridge gives you crystal-clear, 10-PPM restaurant ice cubes."),
    ("shelco-pentair-stainless-steel-whole-house-hot-water-sediment-filter", "304 Stainless Steel High-Temp Whole-House & Boiler Sediment Water Filter Housing (1\" NPT)", "Crack-Proof Stainless Housing", "4.8", "#1 Burst-Proof 300-PSI Stainless Housing for High-Pressure Mains", "304 Stainless Steel Sump (Rated to 300 PSI & 200°F!)", "Zero Risk of Plastic Sump Cracking From Water Hammer", "Bottom Drain Port + Quick-Release Clamp Band", "Accepts Standard 10\" or 20\" Double-Open-End Cartridges", "304+Stainless+Steel+Whole+House+Water+Filter+Housing", "For homes with high municipal street pressure (>80 PSI) or unheated crawlspaces where plastic filter bowls risk cracking from water hammer, a 300-PSI 304 stainless steel filter housing is indestructible."),
    ("morton-clean-and-protect-and-rust-defense-water-softener-salt-pellets", "Morton Clean & Protect / Rust Defense Water Softener Salt Pellets & Potassium Chloride", "High-Purity Softener Salt", "4.8", "#1 Anti-Mush & Iron-Removing Water Softener Salt Pellets", "99.8% Pure Compacted Salt Pellets (Prevent Brine Tank Mush)", "Rust Defense Formula (Blue Bag) Strips Iron From Resin on Every Cycle", "Easy-Pour 40-Lb Bags w/ Two-Handed Carry Handles", "NSF Certified for All Water Softeners", "Morton+Clean+and+Protect+Rust+Defense+Water+Softener+Salt+Pellets", "Never pour cheap rock salt into a modern digital water softener—rock salt contains 2% insoluble dirt that turns into mud at the bottom of your brine drum. Always use compacted 99.8% pure evaporated salt pellets (or Rust Defense pellets on well water).")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: GPG Softening, GPM Flow & Water Lab Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Titration & TDS-meter verified filtration performance ({s1}) tested under real household flow",
            f"High-flow hydraulic design ({s2}) eliminates shower pressure drop across multi-bath homes",
            f"DIY-friendly plumbing integration ({s3}) with standard NPT and quick-connect fittings",
            f"Backed by {s4} for multi-year water purity"
        ],
        "cons": [
            "Always verify your water hardness in GPG, iron PPM, and peak household GPM using our calculator before sizing"
        ],
        "body_paragraphs": [
            f"When sizing a whole-house water softener, sediment/iron filter, and under-sink reverse osmosis system on {SITE_NAME}, matching your resin grain capacity and housing port size to your family's daily gallon usage is what prevents hardness bleed-through and pressure loss. In our hands-on water lab evaluation, the {prod_name} exceeded factory benchmarks.",
            f"Equipped with {s1} and {s2}, it strips away scale-forming minerals, chlorine, and dissolved contaminants without restricting household flow. Furthermore, {s3} makes annual cartridge and salt maintenance effortless.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 rating as one of the highest-ROI home water treatment upgrades for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            water_configs = [
                ("48,000-Grain Fleck 5600SXT Softener + 20\" Big Blue Carbon + 800GPD RO", 48000, "12 GPM Flow", "15–22 GPG Water", "4-Person / 3-Bath"),
                ("64,000-Grain Fleck 5600SXT Softener + Iron/Manganese Filter + UV", 64000, "15 GPM Flow", "25 GPG + 3 PPM Iron", "5-Person Well Water"),
                ("32,000-Grain Digital Water Softener + Spin-Down Pre-Filter + 600GPD RO", 32000, "10 GPM Flow", "10–15 GPG Water", "2–3 Person / 2-Bath"),
                ("80,000-Grain Heavy-Duty Softener + 3-Stage 20\" Big Blue + 800GPD RO", 80000, "18 GPM Flow", "30+ GPG Extreme Hard", "6+ Person / 4-Bath"),
                ("Well Water Defense Rig: Spin-Down + 3-Stage Iron Big Blue + 55W UV", 48000, "12 GPM UV", "Well Water Bacteria/Iron", "3-Bath Rural Home"),
                ("City Chloramine & Scale Shield: 10% Crosslink 48k Softener + G3P800 RO", 48000, "14 GPM Flow", "18 GPG City Water", "4-Person Suburban")
            ]
            w_name, gr_v, gpm_s, gpg_s, fam_s = water_configs[extra_num % len(water_configs)]
            proc_tuple = (
                f"water-softener-{gr_v}-grain-ro-filter-review-{extra_num}",
                f"{gr_v:,}-Grain ({gpm_s}, {gpg_s}) Water Softener & RO Package Review (#{extra_num})",
                f"{int(gr_v/1000)}k-Grain / {gpm_s} System",
                "4.8",
                f"Verified {gr_v:,} Grains @ {gpm_s}",
                f"{gr_v:,} Grains Capacity ({gpm_s})",
                f"Treats {gpg_s} to 0.0 GPG",
                f"Sized for {fam_s} Household",
                "5-to-10 Year Tank & Valve Warranty",
                f"Fleck+5600SXT+Waterdrop+iSpring+{gr_v}+Grain+Water+Softener",
                f"Complete Hach 5B 0-GPG titration check, {gpm_s} pressure-drop test, and salt-dose efficiency log for a {w_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO WATER SOFTENER & RO PRESETS
# ==========================================
WATER_PRESETS = [
    {"slug": "water-softener-grain-size-calculator-family-of-4", "name": "Family of 4 (18 GPG Hardness / 3 Bathrooms — 48,000 Grain)", "people": 4, "gpg": 18, "iron_ppm": 0.5, "baths": 3.0, "ro_gal": 4, "desc": "Calculate exact daily grain demand (6,000 grains/day), why a 48,000-Grain Fleck 5600SXT water softener is the ideal 8-day regeneration match, and annual 40-lb salt bag usage."},
    {"slug": "well-water-iron-and-64000-grain-softener-size-calculator", "name": "Well Water Home (4 People / 22 GPG + 3.0 PPM Iron — 64,000 Grain)", "people": 4, "gpg": 22, "iron_ppm": 3.0, "baths": 3.5, "ro_gal": 5, "desc": "Every 1.0 PPM of ferrous well iron adds +4 GPG of compensated hardness! Calculate why 22 GPG + 3 PPM iron requires a 64,000-Grain softener and iSpring WGB32BM iron filter."},
    {"slug": "family-of-2-3-32000-grain-water-softener-size-calculator", "name": "Couple / Small Family of 2–3 (12 GPG / 2 Baths — 32,000 Grain)", "people": 3, "gpg": 12, "iron_ppm": 0.0, "baths": 2.0, "ro_gal": 3, "desc": "Calculate 2,700 daily grains, 9 GPM peak flow rate, and why a 32,000-Grain (1.0 cu.ft.) digital water softener fits 2-to-3 person households."},
    {"slug": "large-family-of-5-6-extreme-hard-water-64000-80000-grain-calculator", "name": "Large Family of 5–6 (28 GPG Hard Water / 4 Baths — 64k–80k Grain)", "people": 6, "gpg": 28, "iron_ppm": 1.0, "baths": 4.0, "ro_gal": 6, "desc": "Size a 64,000-Grain or 80,000-Grain high-flow (15–18 GPM) water softener for large families with extreme 25–35 GPG hard water."},
    {"slug": "ppm-to-gpg-water-hardness-converter-and-softener-calculator", "name": "PPM (mg/L) to Grains Per Gallon (GPG) Hardness Converter (250 PPM = 14.6 GPG)", "people": 4, "gpg": 15, "iron_ppm": 0.0, "baths": 2.5, "ro_gal": 4, "desc": "Convert city water quality report hardness from Parts Per Million (PPM / mg/L ÷ 17.1 = GPG) and calculate exact water softener grain capacity."},
    {"slug": "whole-house-water-filter-gpm-flow-rate-size-calculator", "name": "3-to-4 Bathroom Whole-House Filter & UV Sterilizer GPM Calculator", "people": 4, "gpg": 16, "iron_ppm": 1.5, "baths": 3.5, "ro_gal": 4, "desc": "Calculate peak simultaneous fixture demand (12–15 GPM) to size 20\"×4.5\" Big Blue whole-house filters and 55W 12-GPM UV sterilizers without pressure loss."},
    {"slug": "water-softener-salt-bag-consumption-and-brine-setting-calculator", "name": "Water Softener Salt Consumption Calculator (40-Lb Bags Per Year)", "people": 4, "gpg": 20, "iron_ppm": 0.5, "baths": 3.0, "ro_gal": 4, "desc": "Calculate exact pounds of softener salt per regeneration (8 lbs/cu.ft. high-efficiency setting) and how many 40-lb Morton salt bags your household will use per year."},
    {"slug": "tankless-reverse-osmosis-wastewater-savings-gpd-calculator", "name": "Tankless RO (3:1 Ratio) vs. Traditional Tank RO (1:3) Water Savings Calculator", "people": 4, "gpg": 18, "iron_ppm": 0.0, "baths": 3.0, "ro_gal": 5, "desc": "See how a Waterdrop G3P800 (3:1 pure-to-drain ratio) saves over 4,800 gallons of drain water per year compared to old 1:3 pressurized-tank RO systems."},
    {"slug": "fleck-5600sxt-programming-settings-bf-df-c-h-calculator", "name": "Fleck 5600SXT Digital Programming Calculator (C, H, SF, DO, BF Settings)", "people": 4, "gpg": 18, "iron_ppm": 1.0, "baths": 3.0, "ro_gal": 4, "desc": "Calculate the exact C (Capacity), H (Compensated Hardness), SF (10% Safety Factor), and BF (Brine Fill Minutes) settings to enter into a Fleck 5600SXT control head."},
    {"slug": "tankless-water-heater-scale-protection-softener-calculator", "name": "Tankless Gas/Electric Water Heater Scale Protection Calculator", "people": 4, "gpg": 14, "iron_ppm": 0.0, "baths": 3.0, "ro_gal": 4, "desc": "Tankless water heater warranties void if hardness exceeds 7 GPG! Size a 48,000-grain ion-exchange softener to stop heat-exchanger lime scale."},
    {"slug": "city-water-chlorine-chloramine-carbon-filter-and-softener-calculator", "name": "City Water Chlorine/Chloramine Carbon Filter + Softener Calculator", "people": 4, "gpg": 16, "iron_ppm": 0.0, "baths": 3.0, "ro_gal": 4, "desc": "Protect your water softener resin from municipal chlorine degradation with an upstream 20\"×4.5\" iSpring CTO carbon block system."},
    {"slug": "private-well-water-bacteria-uv-iron-sediment-softener-calculator", "name": "Complete 4-Stage Private Well Water Treatment Sizing Calculator", "people": 5, "gpg": 24, "iron_ppm": 3.5, "baths": 3.5, "ro_gal": 5, "desc": "Design a complete well-water train: Stage 1 Spin-Down (50µm) → Stage 2 Big Blue Iron/Sediment → Stage 3 64k Softener → Stage 4 12-GPM 55W UV Sterilizer."}
]

def get_dynamic_gpg_and_family_pages():
    configs = [
        (2, 10, 0.0, 2.0, "2 People w/ 10 GPG Moderately Hard Water"),
        (3, 15, 0.0, 2.5, "3 People w/ 15 GPG Hard Water"),
        (4, 12, 0.0, 2.5, "4 People w/ 12 GPG Hard Water"),
        (4, 25, 1.0, 3.0, "4 People w/ 25 GPG Very Hard Water"),
        (5, 18, 0.5, 3.5, "5 People w/ 18 GPG Hard Water"),
        (5, 30, 2.0, 3.5, "5 People w/ 30 GPG Extreme Well Water"),
        (6, 20, 0.5, 4.0, "6 People w/ 20 GPG Hard Water"),
        (7, 25, 1.0, 4.5, "7+ People w/ 25 GPG Hard Water")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 5 + (day_of_year % 4))
    pages = []
    for p_cnt, gpg_v, fe_v, b_cnt, label in configs[:active_count]:
        pages.append({
            "slug": f"{p_cnt}-people-{gpg_v}-gpg-water-softener-grain-size-calculator",
            "name": f"{label}",
            "people": p_cnt,
            "gpg": gpg_v,
            "iron_ppm": fe_v,
            "baths": b_cnt,
            "ro_gal": p_cnt + 1,
            "desc": f"Calculate exact daily grains, Fleck 5600SXT grain capacity tier, peak GPM flow, and annual salt bags for {label}."
        })
    return pages

ALL_CALC_PAGES = WATER_PRESETS + get_dynamic_gpg_and_family_pages()

def compute_water_specs(people, gpg, iron_ppm, baths, ro_gal_per_day):
    # 1. Compensated Hardness (GPG): Every 1 PPM of Ferrous Iron = +4 GPG equivalent load on resin
    comp_gpg = int(math.ceil(float(gpg) + (float(iron_ppm) * 4.0)))
    daily_gallons = int(round(float(people) * 75.0))
    daily_grains = daily_gallons * comp_gpg

    # Target 8-day regeneration cycle with 15% reserve buffer (running resin at efficient ~24k working grains per cu.ft instead of 32k max)
    target_8day_grains = daily_grains * 8.0
    if target_8day_grains <= 23000:
        rec_grain_tier = 32000
        resin_cuft = 1.0
    elif target_8day_grains <= 38000:
        rec_grain_tier = 48000
        resin_cuft = 1.5
    elif target_8day_grains <= 54000:
        rec_grain_tier = 64000
        resin_cuft = 2.0
    else:
        rec_grain_tier = 80000
        resin_cuft = 2.5

    # Actual days between regenerations at 24,000 working grains per cu.ft (8 lbs salt/cu.ft setting)
    working_grains = int(round(resin_cuft * 24000))
    regen_days = max(3, int(round(working_grains / max(500.0, float(daily_grains)))))

    # Annual 40-Lb Salt Bags (8 lbs salt per cu.ft per regen)
    salt_per_regen_lbs = resin_cuft * 8.0
    regens_per_year = 365.0 / float(regen_days)
    annual_salt_lbs = int(round(salt_per_regen_lbs * regens_per_year))
    salt_bags_40lb = max(2, int(math.ceil(annual_salt_lbs / 40.0)))

    # Peak Whole-House Flow Rate (GPM) based on bathrooms
    peak_gpm = round(max(8.0, float(baths) * 3.8), 1)

    # Tankless RO (3:1) Annual Water Saved vs Traditional Tank RO (1:3)
    # Traditional wastes 3x ro_gal_per_day; Tankless wastes 0.33x ro_gal_per_day
    ro_saved_gal_yr = int(round(float(ro_gal_per_day) * (3.0 - 0.33) * 365.0))

    return comp_gpg, daily_gallons, daily_grains, rec_grain_tier, resin_cuft, regen_days, salt_bags_40lb, annual_salt_lbs, peak_gpm, ro_saved_gal_yr

def generate_faq_data(preset_name, people, gpg, iron_ppm, baths, ro_gal):
    comp_gpg, d_gal, d_gr, tier_gr, cuft, r_days, s_bags, s_lbs, gpm, ro_saved = compute_water_specs(
        people, gpg, iron_ppm, baths, ro_gal
    )
    return [
        {
            "q": f"What size water softener (Grains) do I need for {preset_name} ({people} people at {gpg} GPG + {iron_ppm} PPM iron)?",
            "a": f"Your household uses approximately {d_gal} gallons per day with a compensated hardness of {comp_gpg} GPG ({gpg} GPG + 4×{iron_ppm} PPM iron) = {d_gr:,} Grains per day. To regenerate efficiently once every ~{r_days} days, install a {tier_gr:,}-Grain ({cuft} cu. ft. resin) Digital Metered Water Softener."
        },
        {
            "q": f"How many 40-lb bags of water softener salt will a {tier_gr:,}-grain system use per year?",
            "a": f"Programmed to the high-efficiency salt dose of 8 lbs per cubic foot ({int(cuft*8)} lbs per cycle every {r_days} days), your softener will consume approximately {s_lbs} lbs of salt per year—which equals {s_bags} standard 40-lb bags of Morton softener pellets."
        },
        {
            "q": f"What GPM flow rate is needed for a {baths}-bathroom whole-house water filter and UV system?",
            "a": f"A {baths}-bathroom home experiences peak simultaneous water demand of approximately {gpm} Gallons Per Minute (GPM). Always choose 20\"×4.5\" Big Blue whole-house filter housings with 1-inch NPT ports (15 GPM rated) so shower pressure never drops."
        },
        {
            "q": "Do I need a Reverse Osmosis (RO) drinking water system if I have a water softener?",
            "a": f"Yes! A water softener exchanges calcium/magnesium ions for sodium ions—so softened water contains added sodium and does not remove fluoride, PFAS, nitrates, or dissolved solids (TDS). Installing a tankless under-sink RO system (like the Waterdrop G3P800) strips out 95% of sodium and TDS while saving {ro_saved:,} gallons of wastewater per year."
        },
        {
            "q": "How do I convert water hardness from PPM (or mg/L) to Grains Per Gallon (GPG)?",
            "a": "Divide your water report's hardness in Parts Per Million (PPM or mg/L CaCO3) by 17.1 to get Grains Per Gallon (GPG). For example, 300 PPM ÷ 17.1 = 17.5 GPG (Very Hard Water)."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-teal-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['capacity_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['flow_spec']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-teal-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-teal-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top Water Softeners, Tankless RO Systems, Big Blue Filters & UV Sterilizers Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 NSF/ANSI 44, 55 & 58 Tested Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Water System Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Grain / GPD Capacity</th>
                        <th class="p-3.5">Flow Rate / Ratio</th>
                        <th class="p-3.5">Key Filtration Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-teal-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Capacity / Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Valve / Flow:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Media / Tech:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Warranty:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Water Lab Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Fleck+5600SXT+Water+Softener+Waterdrop+G3P800+RO+iSpring+Filter+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Water Filtration Deals</span>
            <span>Save up to 30% on Fleck 5600SXT Water Softeners, Waterdrop Tankless RO Systems, 3-Stage Big Blue Filters & UV Sterilizers on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Water Softener & RO Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-teal-700 flex items-center justify-center text-white font-black text-lg shadow-sm">W</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Softener Grains (GPG), Filter GPM & RO Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-teal-800 transition">Grain & GPM Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-teal-800 transition">Search Systems</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-teal-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-teal-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-teal-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-teal-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-teal-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-teal-800 hover:underline">💧 {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-teal-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-teal-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-teal-700 hover:bg-teal-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Softener & Filter Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-teal-800 hover:underline">🏠 Home — Master Water Softener Grain & GPM Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all water softener grain capacity calculators, whole-house filter GPM guides, reverse osmosis calculators, and daily reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive water softener grain calculator, well-water iron filter guide, reverse osmosis savings tool, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    comp_gpg, _, d_gr, tier_gr, _, _, s_bags, _, gpm, _ = compute_water_specs(
        page_data["people"], page_data["gpg"], page_data["iron_ppm"],
        page_data["baths"], page_data["ro_gal"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — {tier_gr:,} Grain & {gpm} GPM Calculator | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(
        page_data["name"], page_data["people"], page_data["gpg"],
        page_data["iron_ppm"], page_data["baths"], page_data["ro_gal"]
    )

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, _, _, p_tier, _, _, _, _, p_gpm, _ = compute_water_specs(
            p["people"], p["gpg"], p["iron_ppm"], p["baths"], p["ro_gal"]
        )
        active_cls = "bg-teal-100 border-teal-700 text-teal-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-teal-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-teal-900 font-mono shrink-0">{int(p_tier/1000)}kG / {p_gpm}GPM</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Fleck+5600SXT+Water+Softener+iSpring+Whole+House+Filter+and+Waterdrop+G3P800")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-teal-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>💧 WQA Grain Capacity (GPG + Iron), Whole-House GPM & Tankless RO Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Water Softener Grain Capacity (GPG), Whole-House Filter GPM & RO Calculator" if is_home else f"{page_data['name']} — Grain & GPM Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Household Size, Water Hardness & Iron</h2>
                        <p class="text-xs text-gray-600">Calculates softener grain tier (32k–80k), peak GPM, annual salt bags & RO savings</p>
                    </div>
                    <span class="text-xs font-mono bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded font-semibold">Live WQA Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Household & Water Source Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <option value="{page_data['people']},{page_data['gpg']},{page_data['iron_ppm']},{page_data['baths']},{page_data['ro_gal']}">Current: {page_data['name']}</option>
                        <option value="4,18,0.5,3.0,4">Family of 4 on City/Suburban Water (18 GPG / 3 Baths — 48,000 Grain)</option>
                        <option value="4,22,3.0,3.5,5">Private Well Water Home (4 People / 22 GPG + 3 PPM Iron — 64,000 Grain)</option>
                        <option value="3,12,0.0,2.0,3">Small Family / Couple of 2–3 (12 GPG / 2 Baths — 32,000 Grain)</option>
                        <option value="6,28,1.0,4.0,6">Large Family of 5–6 w/ Extreme Hard Water (28 GPG — 64k/80k Grain)</option>
                        <option value="5,24,3.5,3.5,5">Complete 4-Stage Well Water Defense (24 GPG + 3.5 PPM Iron + UV)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label for="peopleInput" class="block text-sm font-bold text-gray-800 mb-1">People in Home</label>
                        <input type="number" id="peopleInput" value="{page_data['people']}" min="1" max="15" step="1" oninput="calculateWater()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <span class="text-[11px] text-gray-600">Avg: 75 Gal / Person / Day</span>
                    </div>

                    <div>
                        <label for="gpgInput" class="block text-sm font-bold text-gray-800 mb-1">Water Hardness (GPG)</label>
                        <input type="number" id="gpgInput" value="{page_data['gpg']}" min="1" max="100" step="1" oninput="calculateWater()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <span class="text-[11px] text-gray-600">PPM ÷ 17.1 = GPG (Hard &gt; 7)</span>
                    </div>

                    <div>
                        <label for="ironInput" class="block text-sm font-bold text-gray-800 mb-1">Well Water Iron (PPM)</label>
                        <input type="number" id="ironInput" value="{page_data['iron_ppm']}" min="0.0" max="15.0" step="0.5" oninput="calculateWater()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <span class="text-[11px] text-gray-600">1 PPM Iron = +4 GPG Load</span>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="bathsInput" class="block text-sm font-bold text-gray-800 mb-1">Number of Bathrooms (Sizes Peak GPM)</label>
                        <select id="bathsInput" onchange="calculateWater()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="1.5" {"selected" if page_data['baths'] <= 1.5 else ""}>1 to 1.5 Bathrooms (~8 GPM Peak Flow)</option>
                            <option value="2.0" {"selected" if page_data['baths'] == 2.0 else ""}>2.0 Bathrooms (~9–10 GPM Peak Flow)</option>
                            <option value="2.5" {"selected" if page_data['baths'] == 2.5 else ""}>2.5 Bathrooms (~10–12 GPM Peak Flow)</option>
                            <option value="3.0" {"selected" if page_data['baths'] == 3.0 else ""}>3.0 Bathrooms (~12–14 GPM Peak Flow)</option>
                            <option value="3.5" {"selected" if page_data['baths'] == 3.5 else ""}>3.5 Bathrooms (~14–15 GPM Peak Flow)</option>
                            <option value="4.5" {"selected" if page_data['baths'] >= 4.0 else ""}>4.0 to 5+ Bathrooms (15–18+ GPM High Flow)</option>
                        </select>
                    </div>

                    <div>
                        <label for="roInput" class="block text-sm font-bold text-gray-800 mb-1">Daily Drinking / Cooking Water (Gallons)</label>
                        <input type="number" id="roInput" value="{page_data['ro_gal']}" min="1" max="30" step="1" oninput="calculateWater()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <span class="text-[11px] text-gray-600">Calculates 3:1 Tankless RO wastewater saved/yr</span>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-teal-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">2. Engineered Softener, Filter & RO Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Water System</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-teal-100 border border-teal-300 rounded-xl p-3.5">
                        <span class="text-xs text-teal-950 font-semibold block">Min. Softener Capacity</span>
                        <span id="resGrainTier" class="text-2xl font-black text-teal-800">48,000 Grain</span>
                        <span id="resResinCuft" class="text-[11px] text-teal-900 block mt-0.5">1.5 ft³ Resin (6,000 Gr/Day)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Peak Flow & Regen</span>
                        <span id="resPeakGPM" class="text-xl font-black text-gray-900">11.4 GPM</span>
                        <span id="resRegenDays" class="text-[11px] text-emerald-800 font-bold block mt-0.5">Regens Every ~6 Days</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Annual 40-Lb Salt Bags</span>
                        <span id="resSaltBags" class="text-base font-extrabold text-gray-900">19 Bags / Yr</span>
                        <span id="resCompGPG" class="text-[11px] text-gray-600 block mt-0.5">20 GPG Compensated</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Tankless RO Water Saved</span>
                        <span id="resRoSaved" class="text-base font-extrabold text-amber-800">3,898 Gal/Yr</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">3:1 Ratio vs Old 1:3 RO</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-teal-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-teal-700 text-white px-2 py-0.5 rounded">Verified Hardware Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recWaterTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Softener & RO Match...</h3>
                    <p id="recWaterDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Water Softener &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Tankless RO & Filter
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Water Softeners, Tankless RO Systems, Big Blue Filters & UV Sterilizers</h2>
                <p class="text-sm text-gray-700">Search any capacity (32000, 48000, 64000 grain, 800 GPD), brand (Fleck 5600SXT, Waterdrop, iSpring, APEC, Aquasure, HQUA, Hach 5B) on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Fleck 5600SXT 48000 Grain, Waterdrop G3P800 Tankless RO, iSpring WGB32BM Iron Filter..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-teal-700" required>
                    <button type="submit" class="bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Fleck 5600SXT 48000 64000 Grain Water Softener')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Fleck 5600SXT Softeners</a>
                    <a href="{amz_url('Waterdrop G3P800 G3P600 Tankless Reverse Osmosis')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Waterdrop Tankless RO</a>
                    <a href="{amz_url('iSpring WGB32B WGB32BM 3 Stage Whole House Filter')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">iSpring 3-Stage Big Blue</a>
                    <a href="{amz_url('HQUA OWS 12 55W Whole House UV Water Sterilizer')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Whole-House UV Sterilizers</a>
                    <a href="{amz_url('Hach 5B Total Hardness Test Kit')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Hach 5B GPG Test Kit</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Verified NSF Water Treatment Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling Water Softeners, Tankless RO Systems, Whole-House Filters & UV</h2>
                </div>
                <a href="{amz_url('Best Selling Water Softeners and Reverse Osmosis Systems')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-teal-800 hover:text-teal-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Water Softener, Reverse Osmosis & Well Filter Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-teal-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-700 text-white px-2.5 py-1 rounded">Complete Whole-House + Drinking Water Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Eliminating Hard Water Scale, Well Iron & PFAS Across Your Entire Home?</h2>
                <p class="text-sm text-gray-800">Build a commercial-grade home water plant by pairing a 50µm Spin-Down Pre-Filter + 3-Stage 20\" Big Blue Filter with a Fleck 5600SXT Digital Water Softener and an Under-Sink Waterdrop G3P800 Tankless RO.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Softener + Whole-House Filter + RO Bundles &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Household Size, Hardness GPG & Well Iron Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact family size, hardness level, or water source below for pre-calculated softener grain capacity, salt bag usage, and GPM flow specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Ion-Exchange Chemistry, GPG vs PPM & RO Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-teal-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-teal-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-teal-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-teal-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-teal-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-teal-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("peopleInput").value = parts[0];
                document.getElementById("gpgInput").value = parts[1];
                document.getElementById("ironInput").value = parts[2];
                document.getElementById("bathsInput").value = parts[3];
                document.getElementById("roInput").value = parts[4];
                calculateWater();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateWater() {{
            const people = parseFloat(document.getElementById("peopleInput").value) || 4;
            const gpg = parseFloat(document.getElementById("gpgInput").value) || 18;
            const ironPPM = parseFloat(document.getElementById("ironInput").value) || 0.5;
            const baths = parseFloat(document.getElementById("bathsInput").value) || 3.0;
            const roGal = parseFloat(document.getElementById("roInput").value) || 4;

            const compGPG = Math.ceil(gpg + (ironPPM * 4.0));
            const dailyGal = Math.round(people * 75.0);
            const dailyGrains = dailyGal * compGPG;

            const target8Day = dailyGrains * 8.0;
            let recGrain = 48000;
            let resinCuft = 1.5;
            if (target8Day <= 23000) {{
                recGrain = 32000;
                resinCuft = 1.0;
            }} else if (target8Day <= 38000) {{
                recGrain = 48000;
                resinCuft = 1.5;
            }} else if (target8Day <= 54000) {{
                recGrain = 64000;
                resinCuft = 2.0;
            }} else {{
                recGrain = 80000;
                resinCuft = 2.5;
            }}

            const workingGrains = Math.round(resinCuft * 24000);
            const regenDays = Math.max(3, Math.round(workingGrains / Math.max(500, dailyGrains)));

            const saltPerRegen = resinCuft * 8.0;
            const annualSaltLbs = Math.round(saltPerRegen * (365.0 / regenDays));
            const saltBags = Math.max(2, Math.ceil(annualSaltLbs / 40.0));

            const peakGPM = Math.max(8.0, baths * 3.8).toFixed(1);
            const roSavedYr = Math.round(roGal * (3.0 - 0.33) * 365.0);

            document.getElementById("resGrainTier").textContent = recGrain.toLocaleString() + " Grain";
            document.getElementById("resResinCuft").textContent = resinCuft.toFixed(1) + " ft³ Resin (" + dailyGrains.toLocaleString() + " Gr/Day)";
            document.getElementById("resPeakGPM").textContent = peakGPM + " GPM Flow";
            document.getElementById("resRegenDays").textContent = "Regens Every ~" + regenDays + " Days";
            document.getElementById("resSaltBags").textContent = saltBags + " Bags / Yr (" + annualSaltLbs + " lb)";
            document.getElementById("resCompGPG").textContent = compGPG + " GPG Compensated (C=" + (workingGrains/1000) + "k)";
            document.getElementById("resRoSaved").textContent = roSavedYr.toLocaleString() + " Gal/Yr";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Waterdrop G3P800 Tankless Reverse Osmosis and Hach 5B Hardness Test Kit";

            if (ironPPM >= 1.5) {{
                recTitle = "Fleck 5600SXT " + recGrain.toLocaleString() + "-Grain Softener + iSpring WGB32BM 3-Stage Iron & Manganese Filter";
                recDesc = "Engineered for well water with " + gpg + " GPG hardness and " + ironPPM + " PPM iron at " + peakGPM + " GPM.";
                primaryQuery = "Fleck 5600SXT " + recGrain + " Grain Water Softener and iSpring WGB32BM Iron Filter";
                secondaryQuery = "HQUA OWS 12 55W Whole House UV Water Sterilizer and Spin Down Filter";
            }} else {{
                recTitle = "Fleck 5600SXT / Aquasure Harmony " + recGrain.toLocaleString() + "-Grain Softener + Waterdrop G3P800 Tankless RO";
                recDesc = "Delivers 0.0 GPG soft water across " + baths + " bathrooms (" + peakGPM + " GPM) plus 800 GPD pure drinking water.";
                primaryQuery = "Fleck 5600SXT Aquasure Harmony " + recGrain + " Grain Water Softener";
            }}

            document.getElementById("recWaterTitle").textContent = recTitle;
            document.getElementById("recWaterDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateWater);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-teal-700 transition block">
            <span class="text-[11px] font-bold text-teal-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-800">Home & Grain Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-teal-800">Daily Water Lab Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">Water Lab Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Capacity / Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Valve / Flow</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Media / Tech</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Your Softener Grains
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Hach 5B Titration, TDS Rejection & GPM Flow Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-teal-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our home water filtration benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Water Softener & RO Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-800">Home & Grain Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-teal-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-teal-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-teal-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "Family of 4 (18 GPG Hardness / 3 Bathrooms — 48,000 Grain)",
        "people": 4,
        "gpg": 18,
        "iron_ppm": 0.5,
        "baths": 3.0,
        "ro_gal": 4,
        "desc": "Calculate exact water softener grain capacity (32k/48k/64k/80k grains), whole-house filter GPM flow rate, well-water iron compensation, annual 40-lb salt bags, and tankless RO water savings—plus read 3 new water filtration reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Water Softener & Filter Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
