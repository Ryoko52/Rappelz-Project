from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route."""
    return render_template('index.html', title='Home')

@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('about.html', title='About')

# Guide routes
@main_bp.route('/guide/getting-started')
def guide_getting_started():
    return render_template('guides/getting_started.html', title='Getting Started in Rappelz')

@main_bp.route('/guide/beyond-master-class')
def guide_beyond_master_class():
    return render_template('guides/beyond_master_class.html', title='Beyond Master Class')

@main_bp.route('/guide/pet-taming')
def guide_pet_taming():
    return render_template('guides/pet_taming.html', title='Pet Taming')

@main_bp.route('/guide/rupee-farming')
def guide_rupee_farming():
    return render_template('guides/rupee_farming.html', title='Rupee Farming')

@main_bp.route('/guide/boss-card-collection')
def guide_boss_card_collection():
    return render_template('guides/boss_card_collection.html', title='Boss Card Collection')

@main_bp.route('/guide/175-and-beyond')
def guide_175_and_beyond():
    return render_template('guides/175_and_beyond.html', title='175 and Beyond')

@main_bp.route('/guide/general-tips')
def guide_general_tips():
    return render_template('guides/general_tips.html', title='General Tips & Tricks')

# Item database routes
# Removed - Items section no longer exists

# Map routes
@main_bp.route('/map/remains-of-the-ancients')
def map_remains():
    return render_template('maps/remains_of_the_ancients.html', title='Remains of the Ancients')

@main_bp.route('/map/snowbasin')
def map_snowbasin():
    return render_template('maps/snowbasin.html', title='SnowBasin')

@main_bp.route('/map/lake-kaia')
def map_lake_kaia():
    return render_template('maps/lake_kaia.html', title='Lake Kaia')

@main_bp.route('/map/pigs-spot')
def map_pigs_spot():
    return render_template('maps/pigs_spot.html', title="Pig's Spot")

# Class routes
@main_bp.route('/class/mercenary')
def class_mercenary():
    return render_template('classes/mercenary.html', title='Mercenary')

@main_bp.route('/class/deadeye')
def class_deadeye():
    return render_template('classes/deadeye.html', title='Deadeye')

@main_bp.route('/class/slayer')
def class_slayer():
    return render_template('classes/slayer.html', title='Slayer')

@main_bp.route('/class/void-mage')
def class_void_mage():
    return render_template('classes/void-mage.html', title='Void Mage')

@main_bp.route('/class/master-breeder')
def class_master_breeder():
    return render_template('classes/master-breeder.html', title='Master Breeder')

@main_bp.route('/class/overlord')
def class_overlord():
    return render_template('classes/overlord.html', title='Overlord')

@main_bp.route('/class/magus')
def class_magus():
    return render_template('classes/magus.html', title='Magus')

@main_bp.route('/class/cardinal')
def class_cardinal():
    return render_template('classes/cardinal.html', title='Cardinal')

@main_bp.route('/class/templar')
def class_templar():
    return render_template('classes/templar.html', title='Templar')

@main_bp.route('/class/berserker')
def class_berserker():
    return render_template('classes/berserker.html', title='Berserker')

@main_bp.route('/class/beast-master')
def class_beast_master():
    return render_template('classes/beast-master.html', title='Beast Master')

@main_bp.route('/class/war-kahuna')
def class_war_kahuna():
    return render_template('classes/war-kahuna.html', title='War Kahuna')

@main_bp.route('/class/corruptor')
def class_corruptor():
    return render_template('classes/corruptor.html', title='Corruptor')

@main_bp.route('/class/marksman')
def class_marksman():
    return render_template('classes/marksman.html', title='Marksman')

@main_bp.route('/class/oracle')
def class_oracle():
    return render_template('classes/oracle.html', title='Oracle')

# Strategy routes
@main_bp.route('/strategy/gnoll-buff')
def strategy_gnoll_buff():
    return render_template('strategies/gnoll_buff.html', title='Gnoll Buff Tips & Tricks')

@main_bp.route('/strategy/legendary-gear')
def strategy_legendary_gear():
    return render_template('strategies/legendary_gear.html', title='Legendary Gear Guide')
