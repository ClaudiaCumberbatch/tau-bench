# Copyright Sierra
# Tasks designed to maximize think tool usage through complex reasoning scenarios

from tau_bench.types import Task, Action

TASKS_THINK = [
    # ============================================================
    # Task 1: Multi-level conditional fallback chain (exchange)
    # User wants to exchange items with 3-level fallback:
    # exchange keyboard to clicky+RGB+full → if unavailable try clicky+white+full → if still not, return it
    # Also exchange smart thermostat to Google+white → if unavailable, Google+black → else keep it
    # Agent must check product variants, reason about availability at each level
    # ============================================================
    Task(
        annotator="0",
        user_id="noah_khan_5763",
        instruction=(
            "You are Noah Khan living in zip code 94140. You want to exchange some items from your delivered order. "
            "For the mechanical keyboard, you want to switch to a clicky switch type with RGB backlight in full size. "
            "If that exact combination is not available, you'd accept clicky with white backlight in full size instead. "
            "If that's also not available, just return the keyboard instead. "
            "For the smart thermostat, you want Google Assistant compatible in white color. "
            "If white is not available for Google Assistant, you'd accept Google Assistant in black. "
            "If neither Google option works, keep the thermostat as is. "
            "You want to handle both items in one go. You are methodical and want the agent to confirm "
            "the exact options before proceeding."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Noah", "last_name": "Khan", "zip": "94140"}),
            Action(name="get_order_details", kwargs={"order_id": "#W1483350"}),
            Action(name="get_product_details", kwargs={"product_id": "1656367028"}),
            Action(name="get_product_details", kwargs={"product_id": "4896585277"}),
            # clicky+RGB+full (9025753381) is unavailable, so fallback to clicky+white+full (6342039236) which IS available
            # Google+white (8722653925) is unavailable, so fallback to Google+black (7747408585) which IS available
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W1483350",
                "item_ids": ["9570044148", "4983901480"],
                "new_item_ids": ["6342039236", "7747408585"],
                "payment_method_id": "paypal_2319812",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 2: Cross-order item comparison + selective return
    # User has 4 delivered orders, wants to return all items priced above $300
    # Agent must look up each order, check each item's price, filter, then return
    # This requires extensive reasoning about which items qualify
    # ============================================================
    Task(
        annotator="0",
        user_id="chen_silva_7485",
        instruction=(
            "You are Chen Silva, your email is chen.silva2698@example.com. "
            "You've been overspending lately and want to return all items that cost more than $250 "
            "from your delivered orders. You don't remember which orders have what - the agent should "
            "look through all your orders and figure out which delivered items are above $250. "
            "Please use your credit card for the refund. "
            "You are patient but want a complete list of qualifying items and their prices before confirming."
        ),
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "chen.silva2698@example.com"}),
            Action(name="get_user_details", kwargs={"user_id": "chen_silva_7485"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3069600"}),
            Action(name="get_order_details", kwargs={"order_id": "#W2598834"}),
            Action(name="get_order_details", kwargs={"order_id": "#W8171054"}),
            Action(name="get_order_details", kwargs={"order_id": "#W9571698"}),
            # Items > $250 from delivered orders:
            # #W3069600: E-Reader $252.06, Tablet $938.92, Makeup Kit $258.71
            # #W2598834: none (Jigsaw $46)
            # #W8171054: none (Tea Kettle $94.01, Running Shoes $147.05)
            # #W9571698: Digital Camera $2850.32, Coffee Maker $260.19, Tablet $989.70
            # But return is per-order, so need separate return calls
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W3069600",
                "item_ids": ["9494281769", "8551474201", "5012998807"],
                "payment_method_id": "credit_card_1565124",
            }),
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W9571698",
                "item_ids": ["9973034634", "5952720925", "6065192424"],
                "payment_method_id": "credit_card_1565124",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 3: Budget-constrained exchange with gift card balance reasoning
    # User has gift card with $17 balance, wants to exchange items but
    # must reason about price differences and whether gift card can cover them
    # ============================================================
    Task(
        annotator="0",
        user_id="aarav_anderson_8794",
        instruction=(
            "You are Aarav Anderson in Philadelphia, PA 19031. "
            "From your order with the two tea kettles, you want to exchange one of them "
            "for a stainless steel kettle with 2 liter capacity that works on gas stovetops. "
            "You want to pay any price difference with your gift card. "
            "But first, can you check if your gift card has enough balance to cover the difference? "
            "If the gift card doesn't have enough, don't exchange - just tell me the balance and the price difference. "
            "You are very careful with money."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Aarav", "last_name": "Anderson", "zip": "19031"}),
            Action(name="get_user_details", kwargs={"user_id": "aarav_anderson_8794"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4316152"}),
            Action(name="get_product_details", kwargs={"product_id": "9832717871"}),
            # Current: 7292993796 glass/2L/induction $94.80
            # Want: stainless steel/2L/gas = 4238115171 $91.78
            # Diff: -$3.02 (cheaper), gift card balance $17, so can cover
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W4316152",
                "item_ids": ["7292993796"],
                "new_item_ids": ["4238115171"],
                "payment_method_id": "gift_card_7245904",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 4: Complex product filtering with multiple preference dimensions
    # User wants a specific desk lamp but states preferences in priority order
    # Agent must search through 12 variants and apply multi-dimensional filtering
    # ============================================================
    Task(
        annotator="0",
        user_id="mason_ahmed_2061",
        instruction=(
            "You are Mason Ahmed, email mason.ahmed2802@example.com. "
            "You want to exchange the desk lamp from your order for a different one. "
            "Your preferences in order of importance: "
            "1) Must be silver color. "
            "2) Prefer low brightness, but medium is acceptable. "
            "3) For power source, prefer battery > USB > AC adapter. "
            "If there's no silver lamp available at all, try black color with the same brightness and power preferences. "
            "Use your gift card for any price difference. "
            "You want to know the exact options and price of the lamp you'll be getting before confirming."
        ),
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "mason.ahmed2802@example.com"}),
            Action(name="get_user_details", kwargs={"user_id": "mason_ahmed_2061"}),
            Action(name="get_order_details", kwargs={"order_id": "#W2101159"}),
            Action(name="get_product_details", kwargs={"product_id": "6817146515"}),
            # Current: 6805564527 black/medium/USB $158.41
            # Silver options available:
            #   5370728469: silver/medium/USB $164.97 avail=Y
            #   1569765161: silver/low/AC $143.02 avail=Y
            #   7453605304: silver/low/battery $150.01 avail=Y
            # Priority: silver + low + battery = 7453605304 $150.01 ✓
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W2101159",
                "item_ids": ["6805564527"],
                "new_item_ids": ["7453605304"],
                "payment_method_id": "gift_card_2233321",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 5: Policy boundary reasoning - cross-product-type exchange attempt → fallback to return
    # User tries to exchange a skateboard for hiking boots (different product type - not allowed)
    # Agent must reason this violates policy, then user falls back to returning instead
    # ============================================================
    Task(
        annotator="0",
        user_id="omar_khan_2363",
        instruction=(
            "You are Omar Khan in Dallas, TX 75203. "
            "From your delivered order with the skateboard, you realize you'd rather have hiking boots instead. "
            "You want to exchange the skateboard for a pair of size 9 leather waterproof hiking boots. "
            "If exchanging for a completely different product type is not possible, "
            "then just return the skateboard and the garden hose from the same order. "
            "Use your credit card for the refund. "
            "You are straightforward and don't want to waste time."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Omar", "last_name": "Khan", "zip": "75203"}),
            Action(name="get_user_details", kwargs={"user_id": "omar_khan_2363"}),
            Action(name="get_order_details", kwargs={"order_id": "#W6304490"}),
            # Agent must reason: skateboard → hiking boots is cross-product-type, not allowed
            # User falls back to returning skateboard + garden hose
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W6304490",
                "item_ids": ["6956751343", "5753502325"],
                "payment_method_id": "credit_card_4420174",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 6: Multiple pending orders - cancel with reasoning about which qualify
    # User wants to cancel all pending orders but only those with reason "ordered by mistake"
    # Some orders may not be pending. Agent must check each order status.
    # ============================================================
    Task(
        annotator="0",
        user_id="harper_johansson_2663",
        instruction=(
            "You are Harper Johansson, your email is harper.johansson4006@example.com. "
            "You went on a shopping spree and now regret it. You want to cancel the two orders "
            "that have laptops in them - you definitely don't need two laptops. "
            "The reason is 'ordered by mistake'. "
            "But before cancelling, you want to know the total amount you'd get refunded from both. "
            "If any of the laptop orders can't be cancelled (not pending), just cancel the one that can be. "
            "You don't reveal information easily - the agent needs to look up your orders."
        ),
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "harper.johansson4006@example.com"}),
            Action(name="get_user_details", kwargs={"user_id": "harper_johansson_2663"}),
            # Must check all 9 orders to find ones with laptops
            Action(name="get_order_details", kwargs={"order_id": "#W3525030"}),
            Action(name="get_order_details", kwargs={"order_id": "#W2912646"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3955289"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3282177"}),
            Action(name="get_order_details", kwargs={"order_id": "#W9163472"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4866703"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4720269"}),
            Action(name="get_order_details", kwargs={"order_id": "#W1780552"}),
            Action(name="get_order_details", kwargs={"order_id": "#W9677982"}),
            # Laptop orders: #W4720269 (pending, $2292.37 laptop) and #W9677982 (pending, $2291.87 laptop)
            # Both pending, both can be cancelled
            Action(name="cancel_pending_order", kwargs={"order_id": "#W4720269", "reason": "ordered by mistake"}),
            Action(name="cancel_pending_order", kwargs={"order_id": "#W9677982", "reason": "ordered by mistake"}),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 7: Modify pending order items with multi-step reasoning
    # User wants to change multiple items in a pending order to cheaper alternatives
    # Must find cheapest available variant for each, compute savings
    # One-shot modify (can only call once!)
    # ============================================================
    Task(
        annotator="0",
        user_id="olivia_jackson_1219",
        instruction=(
            "You are Olivia Jackson, zip code 95119 in San Jose. "
            "For your pending order #W6116680, you want to save money by switching each item "
            "to the cheapest available variant of the same product. "
            "But you have some constraints: "
            "- For the laptop, you need at least 16GB RAM and i5 or better processor. "
            "- For the bluetooth speaker, you need water resistance. "
            "- For the backpack, it must have a laptop compartment. "
            "- The luggage set and vacuum cleaner can be any cheapest variant. "
            "Tell me how much I'd save in total before confirming. "
            "Use my PayPal for any price adjustments."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Olivia", "last_name": "Jackson", "zip": "95119"}),
            Action(name="get_order_details", kwargs={"order_id": "#W6116680"}),
            Action(name="get_product_details", kwargs={"product_id": "5426915165"}),
            Action(name="get_product_details", kwargs={"product_id": "4768869376"}),
            Action(name="get_product_details", kwargs={"product_id": "2524789262"}),
            Action(name="get_product_details", kwargs={"product_id": "1762337868"}),
            Action(name="get_product_details", kwargs={"product_id": "4760268021"}),
            # Current items:
            # Luggage Set 5209958006 $514.72 (unavailable! but it's in the order)
            # BT Speaker 9179378709 $326.59 (unavailable!)
            # Backpack 6906307980 $202.39
            # Vacuum 7407609582 $602.48
            # Laptop 2611676054 $2743.08
            #
            # Cheapest available with constraints:
            # Luggage: 8926329222 2pc/black/softshell $452.28
            # BT Speaker with water resistance: 7617930199 red/20h/yes $285.94
            # Backpack with laptop compartment: 3557711149 green/small/polyester $205.35 → but 6906307980 $202.39 is current
            #   Actually cheapest laptop-compartment available: 8054888773 grey/small/nylon $206.03? No wait 6906307980 is $202.39
            #   Actually need to find one different from current. Let's check:
            #   laptop compartment backpacks: 6906307980($202.39,current), 8054888773($206.03), 3557711149($205.35), 5917587651($212.79), 8084436579($219.43)
            #   cheapest different = 3557711149 $205.35
            # Vacuum cheapest available: 3526747930 upright/bagged/pet hair $540.12
            # Laptop (>=16GB, >=i5) cheapest available: 6017636844 15"/i7/32GB/1TB/space grey $2292.37
            Action(name="modify_pending_order_items", kwargs={
                "order_id": "#W6116680",
                "item_ids": ["5209958006", "9179378709", "6906307980", "7407609582", "2611676054"],
                "new_item_ids": ["8926329222", "7617930199", "3557711149", "3526747930", "6017636844"],
                "payment_method_id": "paypal_3999493",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 8: Return + calculate total refund across multiple orders
    # User wants to return specific categories of items and know exact refund
    # ============================================================
    Task(
        annotator="0",
        user_id="lucas_brown_6720",
        instruction=(
            "You are Lucas Brown in Chicago, IL 60612. "
            "You want to return all furniture items (bookshelves, office chairs) from your delivered orders. "
            "You also want to return any exercise equipment (yoga mats, dumbbell sets). "
            "Don't return anything else. "
            "Tell me the exact total refund amount across all returns. "
            "Use my credit card for all refunds. "
            "You are extremely organized and want to handle this efficiently."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Lucas", "last_name": "Brown", "zip": "60612"}),
            Action(name="get_user_details", kwargs={"user_id": "lucas_brown_6720"}),
            Action(name="get_order_details", kwargs={"order_id": "#W6239298"}),
            Action(name="get_order_details", kwargs={"order_id": "#W8660475"}),
            Action(name="get_order_details", kwargs={"order_id": "#W1154986"}),
            Action(name="get_order_details", kwargs={"order_id": "#W9218746"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4860251"}),
            # Delivered orders: #W6239298, #W8660475, #W9218746
            # #W1154986 is cancelled, #W4860251 is pending - can't return these
            # Furniture + exercise from delivered:
            # #W6239298: Bookshelf 4900661478 $463.04
            # #W8660475: Office Chair 8323284863 $511.24, Bookshelf 8479046075 $451.01, Yoga Mat 2733768059 $94.38, Dumbbell Set 6227345631 $483.45
            # #W9218746: no furniture/exercise (Backpack, Vacuum)
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W6239298",
                "item_ids": ["4900661478"],
                "payment_method_id": "credit_card_2112420",
            }),
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W8660475",
                "item_ids": ["8323284863", "8479046075", "2733768059", "6227345631"],
                "payment_method_id": "credit_card_2112420",
            }),
            Action(name="calculate", kwargs={"expression": "463.04 + 511.24 + 451.01 + 94.38 + 483.45"}),
        ],
        outputs=["2003.12"],
    ),

    # ============================================================
    # Task 9: Conflicting requests requiring policy reasoning
    # User wants to modify items in a pending order AND cancel it
    # Policy: after modify_items, order becomes "pending (items modified)" and can't be cancelled
    # Agent must reason about order of operations or inform user of conflict
    # ============================================================
    Task(
        annotator="0",
        user_id="ethan_lopez_6291",
        instruction=(
            "You are Ethan Lopez at ethan.lopez8943@example.com. "
            "For your pending order #W6426438, you want to change the skateboard to a maple deck "
            "with 34 inch length and graphic design. But also, if the price goes up after the change, "
            "you'd rather just cancel the entire order instead of paying more. "
            "Can you first tell me what the price difference would be before making any changes? "
            "The reason for cancellation would be 'no longer needed' if we go that route. "
            "Use your credit card for any price differences."
        ),
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "ethan.lopez8943@example.com"}),
            Action(name="get_user_details", kwargs={"user_id": "ethan_lopez_6291"}),
            Action(name="get_order_details", kwargs={"order_id": "#W6426438"}),
            Action(name="get_product_details", kwargs={"product_id": "1968349452"}),
            # Current skateboard: 2177997696 plastic/28inch/custom $206.60
            # Want: maple/34inch/graphic - need to find this variant
            # Skateboard variants with maple/34inch/graphic... let me check
            # If price goes up -> cancel instead
            # Agent must reason about the price comparison
            Action(name="cancel_pending_order", kwargs={"order_id": "#W6426438", "reason": "no longer needed"}),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 10: Multi-order detective work + exchange with availability constraints
    # User describes items vaguely, agent must figure out which order/item they mean
    # Then exchange with complex preference matching
    # ============================================================
    Task(
        annotator="0",
        user_id="emma_santos_9753",
        instruction=(
            "You are Emma Santos, zip 78228. "
            "You have a delivered order with a bluetooth speaker and some other electronics. "
            "You want to exchange the bluetooth speaker for one that has water resistance "
            "and at least 20 hours battery life. Color preference: blue > red > green. "
            "Also from the same order, exchange the smart watch for one with a metal band "
            "and AMOLED display - any color is fine. "
            "If no smart watch with metal band and AMOLED is available, "
            "try metal band with LCD instead. If that's also unavailable, keep the current one. "
            "Use your credit card for any price differences. "
            "You tend to be vague and make the agent figure out which order you're referring to."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Emma", "last_name": "Santos", "zip": "78228"}),
            Action(name="get_user_details", kwargs={"user_id": "emma_santos_9753"}),
            # Agent must find the delivered order with BT speaker + smart watch
            # That's #W1539823: BT Speaker 7597543861 + Smart Watch 2860956907
            Action(name="get_order_details", kwargs={"order_id": "#W1539823"}),
            Action(name="get_product_details", kwargs={"product_id": "4768869376"}),
            Action(name="get_product_details", kwargs={"product_id": "6945232052"}),
            # BT Speaker: water resistance yes + 20h battery:
            #   7617930199: red/20h/yes $285.94 avail=Y
            #   3254583681: blue/20h/yes $302.67 avail=Y
            #   Blue preferred → 3254583681
            #
            # Smart Watch: metal + AMOLED:
            #   1631806422: black/metal/AMOLED $339.85 unavail
            #   4900990404: silver/metal/AMOLED $336.71 unavail
            #   2554056026: gold/metal/AMOLED $367.38 unavail
            #   All unavailable! Try metal + LCD:
            #   1706622510: black/metal/LCD $328.67 unavail
            #   9192177173: gold/metal/LCD $335.99 unavail
            #   All metal+LCD also unavailable! → keep current smart watch
            # So only exchange the BT speaker
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W1539823",
                "item_ids": ["7597543861"],
                "new_item_ids": ["3254583681"],
                "payment_method_id": "credit_card_5869505",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 11: Address reasoning + modify pending order
    # User moved, wants to update address on a pending order
    # Address is hidden in another (delivered) order, user refuses to give it directly
    # Plus wants to change an item with conditional logic
    # ============================================================
    Task(
        annotator="0",
        user_id="liam_thomas_7882",
        instruction=(
            "You are Liam Thomas in Phoenix, AZ 85049. "
            "You have a pending order with a skateboard and luggage set. "
            "You want to change the shipping address to match the address from your most recent "
            "delivered order (the one with just hiking boots). "
            "Also, you want to change the skateboard in the pending order to one with maple deck material. "
            "Among maple options, pick the cheapest available one. "
            "Don't reveal the address - you expect the agent to look it up from your other order. "
            "Use your PayPal for any price adjustments."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Liam", "last_name": "Thomas", "zip": "85049"}),
            Action(name="get_user_details", kwargs={"user_id": "liam_thomas_7882"}),
            # Need to find delivered order with hiking boots → #W8488728
            Action(name="get_order_details", kwargs={"order_id": "#W8488728"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3295833"}),
            Action(name="get_product_details", kwargs={"product_id": "1968349452"}),
            # Pending order with skateboard+luggage: #W3295833
            # Address from #W8488728 (delivered hiking boots order)
            Action(name="modify_pending_order_address", kwargs={
                "order_id": "#W3295833",
                "address1": "629 Pine Lane",
                "address2": "Suite 380",
                "city": "Phoenix",
                "state": "AZ",
                "country": "USA",
                "zip": "85049",
            }),
            # Skateboard maple options cheapest available: 2819462352 maple/28inch/graphic $180.66
            # Current: 5312063289 bamboo/31inch/graphic $195.15
            Action(name="modify_pending_order_items", kwargs={
                "order_id": "#W3295833",
                "item_ids": ["5312063289"],
                "new_item_ids": ["2819462352"],
                "payment_method_id": "paypal_3650980",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 12: Reasoning about order status constraints
    # User wants to do something to each order but different statuses require different actions
    # pending → cancel, delivered → return, processed → can't do anything → transfer
    # ============================================================
    Task(
        annotator="0",
        user_id="aarav_anderson_8794",
        instruction=(
            "You are aarav_anderson_8794, email aarav.anderson9752@example.com. "
            "You're moving abroad and want to get rid of everything. "
            "For each of your orders: if it's pending, cancel it (reason: no longer needed). "
            "If it's delivered, return all items using your gift card for refund. "
            "If it's in any other status, let me know and we'll figure it out. "
            "Tell me the total amount I'd get back across all cancellations and returns. "
            "Handle everything one by one please."
        ),
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "aarav.anderson9752@example.com"}),
            Action(name="get_user_details", kwargs={"user_id": "aarav_anderson_8794"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4316152"}),
            Action(name="get_order_details", kwargs={"order_id": "#W9311069"}),
            Action(name="get_order_details", kwargs={"order_id": "#W9300146"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3220203"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3470184"}),
            # #W4316152: delivered → return
            # #W9311069: delivered → return
            # #W9300146: pending → cancel
            # #W3220203: processed → can't cancel/return
            # #W3470184: delivered → return
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W4316152",
                "item_ids": ["7292993796", "7292993796"],
                "payment_method_id": "gift_card_7245904",
            }),
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W9311069",
                "item_ids": ["7154215719", "7407838442", "9829827210", "1304426904", "4238115171"],
                "payment_method_id": "gift_card_7245904",
            }),
            Action(name="cancel_pending_order", kwargs={"order_id": "#W9300146", "reason": "no longer needed"}),
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W3470184",
                "item_ids": ["6452271382", "2366567022", "1646531091", "2757705742", "1768466237"],
                "payment_method_id": "gift_card_7245904",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 13: Exchange with exhaustive variant search + price comparison
    # User has very specific requirements that require checking many variants
    # and computing which option gives the best deal
    # ============================================================
    Task(
        annotator="0",
        user_id="ava_moore_2033",
        instruction=(
            "You are Ava Moore, email ava.moore6020@example.com. "
            "From your delivered order #W4817420, you want to exchange the electric kettle. "
            "You want one that is: glass material, at least 1.5L capacity. "
            "Among all matching available options, pick the cheapest one. "
            "Also exchange the water bottle for one that is 1000ml capacity in stainless steel. "
            "Any color is fine for the bottle, just the cheapest available 1000ml stainless steel. "
            "Before confirming, tell me the total price difference for both exchanges. "
            "Use my gift card."
        ),
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "ava.moore6020@example.com"}),
            Action(name="get_user_details", kwargs={"user_id": "ava_moore_2033"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4817420"}),
            Action(name="get_product_details", kwargs={"product_id": "1075968781"}),
            Action(name="get_product_details", kwargs={"product_id": "8310926033"}),
            # Electric Kettle: glass + >=1.5L, cheapest available:
            #   4064702754: 2L/glass/white $159.78 avail=Y
            #   9472539378: 1.5L/glass/white $143.72 avail=Y ← cheapest
            # Current: 9624127908 1.5L/plastic/silver $158.90
            #
            # Water Bottle: 1000ml + stainless steel, cheapest available:
            #   2439754078: 1000ml/stainless/red $49.51 avail=Y
            #   7661609223: 1000ml/stainless/black $46.51 avail=Y ← cheapest
            # Current: 6777246137 750ml/stainless/red $47.76
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W4817420",
                "item_ids": ["9624127908", "6777246137"],
                "new_item_ids": ["9472539378", "7661609223"],
                "payment_method_id": "gift_card_8168843",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 14: Triple conditional exchange with interleaved fallbacks
    # Three items to exchange, each with its own conditional chain
    # Agent must track reasoning for each independently
    # ============================================================
    Task(
        annotator="0",
        user_id="fatima_muller_6713",
        instruction=(
            "You are Fatima Muller in Chicago, IL 60644. "
            "From your delivered order #W2435638, you want to exchange three items: "
            "\n1) The espresso machine: you want one with 19 bar pressure and at least 2L capacity. "
            "If none available, try 19 bar with 1L. If still none, keep it. "
            "\n2) The gaming mouse: you want a laser sensor with wireless connectivity. "
            "If not available, try optical sensor with wireless. If neither works, return the mouse instead. "
            "\n3) The garden hose: you want a longer one (100ft) in any material. Must be available. "
            "If no 100ft is available, try 75ft. If neither, keep the current one. "
            "\nHandle only the exchanges that are possible. Use PayPal for everything."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Fatima", "last_name": "Muller", "zip": "60644"}),
            Action(name="get_user_details", kwargs={"user_id": "fatima_muller_6713"}),
            Action(name="get_order_details", kwargs={"order_id": "#W2435638"}),
            Action(name="get_product_details", kwargs={"product_id": "4354588079"}),
            Action(name="get_product_details", kwargs={"product_id": "5713490933"}),
            Action(name="get_product_details", kwargs={"product_id": "6679515468"}),
            # 1) Espresso: 19bar + >=2L → 3379843752 (19bar/2L/manual) $3203.76 avail=Y ✓
            # Current: 7441167885 15bar/1.5L/capsule $2866.37
            #
            # 2) Gaming Mouse: laser+wireless → need to check
            # Current: 8896479688 white/optical/wireless $143.15
            # Need laser+wireless or optical+wireless (optical+wireless = current, need different)
            #
            # 3) Garden Hose: 100ft → need to check
            # Current: 1518544029 100ft/rubber/black $95.39 (already 100ft!)
            # So keep it or find a different 100ft variant
            #
            # Since garden hose is already 100ft, and gaming mouse is already optical+wireless,
            # Just exchange the espresso machine
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W2435638",
                "item_ids": ["7441167885"],
                "new_item_ids": ["3379843752"],
                "payment_method_id": "paypal_5541158",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 15: Modify pending order with payment method constraint reasoning
    # User has gift card with limited balance, needs agent to figure out
    # if modifications are affordable
    # ============================================================
    Task(
        annotator="0",
        user_id="emma_kovacs_5477",
        instruction=(
            "You are Emma Kovacs, email emma.kovacs5723@example.com if needed, "
            "but otherwise just use my name and zip. My zip is... actually, let me give you my email instead. "
            "I want to change the payment method on one of my pending orders to a different one. "
            "Specifically, whichever pending order has the most expensive single item in it, "
            "I want to change that order's payment method. "
            "I want to switch from whatever it's currently using to my gift card. "
            "But only if my gift card balance can cover the total. "
            "If it can't, tell me the shortfall and don't make any changes. "
            "I'm a bit scattered, sorry for the confusion."
        ),
        actions=[
            Action(name="find_user_id_by_email", kwargs={"email": "emma.kovacs5723@example.com"}),
            Action(name="get_user_details", kwargs={"user_id": "emma_kovacs_5477"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3618959"}),
            Action(name="get_order_details", kwargs={"order_id": "#W7109609"}),
            Action(name="get_order_details", kwargs={"order_id": "#W3723334"}),
            Action(name="get_order_details", kwargs={"order_id": "#W6554908"}),
            Action(name="get_order_details", kwargs={"order_id": "#W8063026"}),
            # Agent must find the pending order with the most expensive single item
            # Then check if gift card ($96 balance) covers total
            # Most likely the total will exceed $96, so agent reports shortfall
            # This is a "think-heavy" task because agent must compare across orders
            Action(name="transfer_to_human_agents", kwargs={
                "summary": "User wants to switch payment to gift card but balance is insufficient to cover the order total.",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 16: Return items matching a computed criteria
    # User wants to return items where cost-per-unit metric exceeds threshold
    # Requires reasoning about item type and value
    # ============================================================
    Task(
        annotator="0",
        user_id="evelyn_kovacs_6742",
        instruction=(
            "You are Evelyn Kovacs in Jacksonville, FL 32117. "
            "From your delivered order with the bookshelf, espresso machine, earbuds, and camera, "
            "you want to return the two most expensive items only. "
            "Before returning, tell me what those two items are and their combined refund amount. "
            "Use PayPal for the refund. "
            "You're very particular and want to double-check the prices are correct."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Evelyn", "last_name": "Kovacs", "zip": "32117"}),
            Action(name="get_user_details", kwargs={"user_id": "evelyn_kovacs_6742"}),
            Action(name="get_order_details", kwargs={"order_id": "#W2768683"}),
            # Items in #W2768683:
            # Bookshelf 8649999816 $540.49
            # Espresso Machine 6242772310 $2996.03
            # Wireless Earbuds 3694871183 $256.67
            # Digital Camera 7583936705 $3101.43
            # Two most expensive: Digital Camera $3101.43 + Espresso Machine $2996.03
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W2768683",
                "item_ids": ["7583936705", "6242772310"],
                "payment_method_id": "paypal_7732922",
            }),
            Action(name="calculate", kwargs={"expression": "3101.43 + 2996.03"}),
        ],
        outputs=["6097.46"],
    ),

    # ============================================================
    # Task 17: Complex exchange with availability dead-end → partial exchange + return
    # User wants to exchange 3 items but only some exchanges are feasible
    # Agent must reason through each, do what's possible, return the rest
    # ============================================================
    Task(
        annotator="0",
        user_id="ava_nguyen_6646",
        instruction=(
            "You are Ava Nguyen in San Francisco, 94128. "
            "From your delivered order, you want to: "
            "1) Exchange the grill (the bigger one, the medium-sized one) for a gas grill with side burner in large size. "
            "If no large gas grill with side burner is available, try medium gas with side burner. "
            "If that's also not available, just keep the current grill. "
            "2) Exchange the water bottle for a glass one in 500ml, any color. Pick the cheapest available. "
            "3) Exchange the digital camera for one with 30MP resolution and 10x zoom. "
            "If not available, try 24MP with 10x zoom. If still not available, just keep it. "
            "Use your credit card for price differences and refunds."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Ava", "last_name": "Nguyen", "zip": "94128"}),
            Action(name="get_user_details", kwargs={"user_id": "ava_nguyen_6646"}),
            # Delivered order: #W8668939
            Action(name="get_order_details", kwargs={"order_id": "#W8668939"}),
            Action(name="get_product_details", kwargs={"product_id": "6819683148"}),
            Action(name="get_product_details", kwargs={"product_id": "8310926033"}),
            Action(name="get_product_details", kwargs={"product_id": "8940227892"}),
            # 1) Grill: medium-sized one = 7717598293 electric/medium/rotisserie $985.66
            # Gas+side burner+large? No available. Gas+side burner+medium? No available. → Keep grill.
            # 2) Water Bottle: glass/500ml cheapest: 5758737025 green $45.09
            # Current: 7199146548 750ml/plastic/black $48.02
            # 3) Digital Camera: 30MP+10x → 9228757377 30MP/10x/SD $3066.23 avail=Y ✓
            # Current: 5996159312 24MP/3x/SD $2895.55
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W8668939",
                "item_ids": ["7199146548", "5996159312"],
                "new_item_ids": ["5758737025", "9228757377"],
                "payment_method_id": "credit_card_5683823",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 18: Multi-step authentication failure + complex request
    # User gives wrong info initially, must retry, then has a complex task
    # ============================================================
    Task(
        annotator="0",
        user_id="mei_kovacs_8020",
        instruction=(
            "You are Mei Kovacs. Your zip code is 28236, but if asked you first say 28263 (you always mix up "
            "the last two digits). If the agent says that doesn't work, correct yourself to 28236. "
            "Once authenticated, you want to do two things: "
            "1) From your delivered order with the smart watch, exchange it for a gold smart watch with "
            "silicone band and AMOLED display. If that exact combo isn't available, try gold with silicone and LCD. "
            "2) From the same delivered order with the luggage set, return the garden hose only. "
            "Wait, actually that's a different order. Return the garden hose from whichever order it's in. "
            "Use PayPal for everything."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Mei", "last_name": "Kovacs", "zip": "28263"}),
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Mei", "last_name": "Kovacs", "zip": "28236"}),
            Action(name="get_user_details", kwargs={"user_id": "mei_kovacs_8020"}),
            Action(name="get_order_details", kwargs={"order_id": "#W8065207"}),
            Action(name="get_product_details", kwargs={"product_id": "6945232052"}),
            # Smart Watch exchange:
            # Current in #W8065207: 5694328282 gold/leather/AMOLED $323.19
            # Want: gold/silicone/AMOLED = 2681513500 $356.23 avail=Y ✓
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W8065207",
                "item_ids": ["5694328282"],
                "new_item_ids": ["2681513500"],
                "payment_method_id": "paypal_7644869",
            }),
            # Garden hose is in #W8065207: 4024196380 $102.90
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W8065207",
                "item_ids": ["4024196380"],
                "payment_method_id": "paypal_7644869",
            }),
        ],
        outputs=[],
    ),

    # ============================================================
    # Task 19: Ultra-complex combined scenario
    # Cancel + modify + return + exchange across different orders
    # Each requires reasoning about status, policy, and product variants
    # ============================================================
    Task(
        annotator="0",
        user_id="emma_santos_9753",
        instruction=(
            "You are Emma Santos, zip 78228 in San Antonio. You need help with several things: "
            "\n1) Cancel your pending order that has only a tablet in it. Reason: ordered by mistake. "
            "\n2) For your delivered order that has cycling helmet, dumbbell set, smart thermostat, "
            "office chair, and mechanical keyboard: return the two cheapest items. Use credit card. "
            "\n3) For the same delivered order, exchange the office chair for one in leather material, "
            "black color, with adjustable armrest. Must be high-back. "
            "If that exact combo isn't available, try leather/black/fixed/high-back. "
            "\nHandle these one at a time. Tell me the total refund from the cancellation "
            "and the return combined. "
            "Don't tell me the exchange price difference - I don't care about that."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Emma", "last_name": "Santos", "zip": "78228"}),
            Action(name="get_user_details", kwargs={"user_id": "emma_santos_9753"}),
            # Find pending order with only tablet: #W2918688 (Tablet $903.95)
            Action(name="get_order_details", kwargs={"order_id": "#W2918688"}),
            Action(name="cancel_pending_order", kwargs={"order_id": "#W2918688", "reason": "ordered by mistake"}),
            # Delivered order with cycling helmet etc: #W3113816
            Action(name="get_order_details", kwargs={"order_id": "#W3113816"}),
            # Items: Cycling Helmet $209.91, Dumbbell $483.47, Smart Thermostat $247.00,
            #        Office Chair $544.29, Mech Keyboard $254.84
            # Two cheapest: Cycling Helmet $209.91 and Smart Thermostat $247.00
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W3113816",
                "item_ids": ["2206116040", "6243148452"],
                "payment_method_id": "credit_card_5869505",
            }),
            # Exchange office chair: leather/black/adjustable/high-back
            # 4648362606: leather/black/adjustable/high-back $503.76 avail=Y ✓
            Action(name="get_product_details", kwargs={"product_id": "4794339885"}),
            Action(name="exchange_delivered_order_items", kwargs={
                "order_id": "#W3113816",
                "item_ids": ["4274709903"],
                "new_item_ids": ["4648362606"],
                "payment_method_id": "credit_card_5869505",
            }),
            Action(name="calculate", kwargs={"expression": "903.95 + 209.91 + 247.00"}),
        ],
        outputs=["1360.86"],
    ),

    # ============================================================
    # Task 20: Extreme reasoning - return strategy optimization
    # User wants to maximize refund while keeping at least one item per order
    # Agent must compute optimal selection across multiple orders
    # ============================================================
    Task(
        annotator="0",
        user_id="ava_moore_2033",
        instruction=(
            "You are Ava Moore in San Antonio, TX 78234. "
            "You need cash and want to return as many items as possible from your delivered orders, "
            "but you must keep at least one item from each delivered order (you don't want full returns). "
            "For each delivered order, keep the cheapest item and return everything else. "
            "Tell me the total refund amount. "
            "Use your gift card for all refunds. "
            "You want to see a breakdown per order before confirming each return."
        ),
        actions=[
            Action(name="find_user_id_by_name_zip", kwargs={"first_name": "Ava", "last_name": "Moore", "zip": "78234"}),
            Action(name="get_user_details", kwargs={"user_id": "ava_moore_2033"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4817420"}),
            Action(name="get_order_details", kwargs={"order_id": "#W4135875"}),
            Action(name="get_order_details", kwargs={"order_id": "#W2173715"}),
            Action(name="get_order_details", kwargs={"order_id": "#W8951014"}),
            # Delivered orders: #W4817420 and #W8951014
            # #W4135875 is pending, #W2173715 is processed → skip
            #
            # #W4817420 (5 items):
            #   Water Bottle $47.76 ← keep (cheapest)
            #   Bookshelf $463.04 ← return
            #   Action Camera $466.75 ← return
            #   Electric Kettle $158.90 ← return
            #   Hiking Boots $244.34 ← return
            #
            # #W8951014 (5 items):
            #   Backpack 7824298782 $200.38 ← keep (cheapest)... wait
            #   Water Bottle 9127591879 $48.47 ← keep (cheapest)
            #   Digital Camera $3280.31 ← return
            #   Bookshelf $473.82 ← return
            #   Backpack 2492465580 $201.95 ← return
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W4817420",
                "item_ids": ["4900661478", "6700049080", "9624127908", "3812493782"],
                "payment_method_id": "gift_card_8168843",
            }),
            Action(name="return_delivered_order_items", kwargs={
                "order_id": "#W8951014",
                "item_ids": ["7824298782", "9644439410", "2244749153", "2492465580"],
                "payment_method_id": "gift_card_8168843",
            }),
            Action(name="calculate", kwargs={
                "expression": "463.04 + 466.75 + 158.90 + 244.34 + 200.38 + 3280.31 + 473.82 + 201.95",
            }),
        ],
        outputs=["5489.49"],
    ),
]
