"""Unit tests for Ants Vs. SomeBees."""

import unittest
import doctest
import os
import sys
import imp
from ucb import main
import ants
import autograder

__version__ = '1.4'


class AntTest(unittest.TestCase):

    def setUp(self):
        hive, layout = ants.Hive(ants.make_test_assault_plan()), ants.test_layout
        self.colony = ants.AntColony(None, hive, ants.ant_types(), layout)


class TestProblem2(AntTest):

    def test_food_costs(self):
        error_msg = "Wrong food_cost for ant class"
        self.assertEqual(2, ants.HarvesterAnt.food_cost, error_msg)
        self.assertEqual(4, ants.ThrowerAnt.food_cost, error_msg)

    def test_harvester(self):
        error_msg = "HarvesterAnt did not add one food"
        old_food = self.colony.food
        ants.HarvesterAnt().action(self.colony)
        self.assertEqual(old_food + 1, self.colony.food, error_msg)


class TestProblem3(AntTest):

    def test_connectedness(self):
        error_msg = "Entrances not properly initialized"
        for entrance in self.colony.bee_entrances:
            place = entrance
            while place:
                self.assertIsNotNone(place.entrance, msg=error_msg)
                place = place.exit

    def test_exits_and_entrances_are_different(self):
        for place in self.colony.places.values():
            self.assertIsNot(place, place.exit,
                             '{0} is its own exit'.format(place))
            self.assertIsNot(place, place.entrance,
                             '{0} is its own entrance'.format(place))
            if place.exit and place.entrance:
                self.assertIsNot(place.exit, place.entrance,
                                 '{0} entrance is its exit'.format(place))


class TestProblemA4(AntTest):

    def test_water_deadliness(self):
        error_msg = "Water does not kill non-watersafe Insects"
        test_ant = ants.HarvesterAnt()
        test_water = ants.Water("water_TestProblemA4_0")
        test_water.add_insect(test_ant)
        self.assertIsNot(test_ant, test_water.ant, msg=error_msg)
        self.assertEqual(0, test_ant.armor, msg=error_msg)

    def test_water_deadliness_with_big_soggy_bee(self):
        error_msg = "Water does not hurt all non-watersafe Insects"
        test_ants = [ants.Bee(1000000), ants.HarvesterAnt(), ants.Ant(),
                     ants.ThrowerAnt()]
        test_ants[0].watersafe = False # Make the Bee non-watersafe
        test_water = ants.Water("water_TestProblemA4_0")
        for test_ant in test_ants:
            test_water.add_insect(test_ant)
            self.assertIsNot(test_ant, test_water.ant, msg=error_msg)
            self.assertIs(0, test_ant.armor, msg=error_msg)

    def test_water_safety(self):
        error_msg = "Water kills watersafe Insects"
        test_bee = ants.Bee(1)
        test_water = ants.Water("water_testProblemA4_0")
        test_water.add_insect(test_bee)
        self.assertIn(test_bee, test_water.bees, msg=error_msg)

    def test_water_inheritance(self):
        error_msg = "It seems Water.add_insect is not using inheritance"
        old_add_insect = ants.Place.add_insect
        def new_add_insect(self, insect):
            raise NotImplementedError()
        ants.Place.add_insect = new_add_insect
        test_bee = ants.Bee(1)
        test_water = ants.Water("water_testProblemA4_0")
        failed = True
        try:
            test_water.add_insect(test_bee)
        except NotImplementedError:
            failed = False
        finally:
            ants.Place.add_insect = old_add_insect
        if failed:
            self.fail(msg=error_msg)

    def test_water_inheritance_ant(self):
        error_msg = "Make sure to place the ant before watering it"
        old_add_insect = ants.Place.add_insect
        def new_add_insect(self, insect):
            raise NotImplementedError()
        ants.Place.add_insect = new_add_insect
        test_ant = ants.HarvesterAnt()
        test_water = ants.Water("water_testProblemA4_0")
        failed = True
        try:
            test_water.add_insect(test_ant)
        except NotImplementedError:
            failed = False
        finally:
            ants.Place.add_insect = old_add_insect
        if failed:
            self.fail(msg=error_msg)


class TestProblemA5(AntTest):

    def test_fire_parameters(self):
        fire = ants.FireAnt()
        self.assertEqual(4, ants.FireAnt.food_cost, "FireAnt has wrong cost")
        self.assertEqual(1, fire.armor, "FireAnt has wrong armor value")

    def test_fire_damage(self):
        error_msg = "FireAnt does the wrong amount of damage"
        place = self.colony.places["tunnel_0_0"]
        bee = ants.Bee(5)
        place.add_insect(bee)
        place.add_insect(ants.FireAnt())
        bee.action(self.colony)
        self.assertEqual(2, bee.armor, error_msg)

    def test_fire_deadliness(self):
        error_msg = "FireAnt does not damage all Bees in its Place"
        test_place = self.colony.places["tunnel_0_0"]
        bee = ants.Bee(3)
        test_place.add_insect(bee)
        test_place.add_insect(ants.Bee(3))
        test_place.add_insect(ants.FireAnt())
        bee.action(self.colony)
        self.assertEqual(0, len(test_place.bees), error_msg)

    def test_fire_damage_is_instance_attribute(self):
        error_msg = "FireAnt damage is not looked up on the instance"
        place = self.colony.places["tunnel_0_0"]
        bee = ants.Bee(900)
        place.add_insect(bee)
        buffAnt = ants.FireAnt()
        buffAnt.damage = 500  # Feel the burn!
        place.add_insect(buffAnt)
        bee.action(self.colony)
        self.assertEqual(400, bee.armor, error_msg)

    def test_fireant_expiration(self):
        error_msg = "FireAnt should have, but did not expire"
        place = self.colony.places["tunnel_0_0"]
        bee = ants.Bee(1)
        place.add_insect(bee)
        ant = ants.FireAnt()
        place.add_insect(ant)
        bee.action(self.colony)
        self.assertEqual(ant.armor, 0, error_msg)


class TestProblemB4(AntTest):

    def test_nearest_bee(self):
        error_msg = "ThrowerAnt can't find the nearest bee"
        ant = ants.ThrowerAnt()
        self.colony.places["tunnel_0_0"].add_insect(ant)
        near_bee = ants.Bee(2)
        self.colony.places["tunnel_0_3"].add_insect(near_bee)
        self.colony.places["tunnel_0_6"].add_insect(ants.Bee(2))
        hive = self.colony.hive
        self.assertIs(ant.nearest_bee(hive), near_bee, error_msg)
        ant.action(self.colony)
        self.assertEqual(1, near_bee.armor, error_msg)

    def test_nearest_bee_not_in_hive(self):
        error_msg = "ThrowerAnt hit a Bee in the Hive"
        ant = ants.ThrowerAnt()
        self.colony.places["tunnel_0_0"].add_insect(ant)
        hive = self.colony.hive
        hive.add_insect(ants.Bee(2))
        self.assertIsNone(ant.nearest_bee(hive), error_msg)

    def test_melee(self):
        error_msg = "ThrowerAnt doesn't attack bees on its own square."
        ant = ants.ThrowerAnt()
        self.colony.places["tunnel_0_0"].add_insect(ant)
        near_bee = ants.Bee(2)
        self.colony.places["tunnel_0_0"].add_insect(near_bee)
        self.assertIs(ant.nearest_bee(self.colony.hive), near_bee, error_msg)
        ant.action(self.colony)
        self.assertIs(1, near_bee.armor, error_msg)

    def test_random_shot(self):
        error_msg = "ThrowerAnt does not appear to choose random targets"
        ant = ants.ThrowerAnt()
        self.colony.places["tunnel_0_0"].add_insect(ant)
        # Place two ultra-bees to test randomness.
        bee = ants.Bee(1001)
        self.colony.places["tunnel_0_3"].add_insect(bee)
        self.colony.places["tunnel_0_3"].add_insect(ants.Bee(1001))
        # Throw 1000 times. The first bee should take ~1000*1/2 = ~500 damage,
        # and have ~501 remaining.
        for _ in range(1000):
            ant.action(self.colony)
        # Test if damage to bee 1 is within 6 standard deviations (~95 damage)
        # If bees are chosen uniformly, this is true 99.9999998% of the time.
        def dmg_within_tolerance():
            return abs(bee.armor-501) < 95
        self.assertIs(True, dmg_within_tolerance(), error_msg)


class TestProblemB5(AntTest):

    def test_thrower_parameters(self):
        short_t = ants.ShortThrower()
        long_t = ants.LongThrower()
        self.assertEqual(3, ants.ShortThrower.food_cost, "ShortThrower has wrong cost")
        self.assertEqual(3, ants.LongThrower.food_cost, "LongThrower has wrong cost")
        self.assertEqual(1, short_t.armor, "ShortThrower has wrong armor")
        self.assertEqual(1, long_t.armor, "LongThrower has wrong armor")

    def test_inheritance(self):
        """Tests to see if the Long and Short Throwers are actually using the
        inherited action from the ThrowerAnt.
        """
        old_thrower_action = ants.ThrowerAnt.action
        old_throw_at = ants.ThrowerAnt.throw_at
        def new_thrower_action(self, colony):
            raise NotImplementedError()
        def new_throw_at(self, target):
            raise NotImplementedError()

        failed_long = 0
        try: # Test action
            ants.ThrowerAnt.action = new_thrower_action
            test_long = ants.LongThrower()
            test_long.action(self.colony)
        except NotImplementedError:
            failed_long += 1
        finally:
            ants.ThrowerAnt.action = old_thrower_action

        try: # Test throw_at
            ants.ThrowerAnt.throw_at = new_throw_at
            test_long = ants.LongThrower()
            test_bee = ants.Bee(1)
            test_long.throw_at(test_bee)
        except NotImplementedError:
            failed_long += 1
        finally:
            ants.ThrowerAnt.throw_at = old_throw_at

        if failed_long < 2:
            self.fail(msg="LongThrower is not using inheritance")

        failed_short = 0
        try: # Test action
            ants.ThrowerAnt.action = new_thrower_action
            test_short = ants.ShortThrower()
            test_short.action(self.colony)
        except NotImplementedError:
            failed_short += 1
        finally:
            ants.ThrowerAnt.action = old_thrower_action

        try: # Test throw_at
            ants.ThrowerAnt.throw_at = new_throw_at
            test_short = ants.ShortThrower()
            test_bee = ants.Bee(1)
            test_short.throw_at(test_bee)
        except NotImplementedError:
            failed_short += 1
        finally:
            ants.ThrowerAnt.throw_at = old_throw_at

        if failed_short < 2:
            self.fail(msg="ShortThrower is not using inheritance")

    def test_long(self):
        error_msg = "LongThrower has the wrong range"
        ant = ants.LongThrower()
        self.colony.places["tunnel_0_0"].add_insect(ant)
        out_of_range, in_range = ants.Bee(2), ants.Bee(2)
        self.colony.places["tunnel_0_3"].add_insect(out_of_range)
        self.colony.places["tunnel_0_4"].add_insect(in_range)
        ant.action(self.colony)
        self.assertEqual(in_range.armor, 1, error_msg)
        self.assertEqual(out_of_range.armor, 2, error_msg)

    def test_short(self):
        error_msg = "ShortThrower has the wrong range"
        ant = ants.ShortThrower()
        self.colony.places["tunnel_0_0"].add_insect(ant)
        out_of_range, in_range = ants.Bee(2), ants.Bee(2)
        self.colony.places["tunnel_0_3"].add_insect(out_of_range)
        self.colony.places["tunnel_0_2"].add_insect(in_range)
        ant.action(self.colony)
        self.assertEqual(in_range.armor, 1, error_msg)
        self.assertEqual(out_of_range.armor, 2, error_msg)

    def test_instance_range(self):
        error_msg = "Range is not looked up on the instance"
        #Buff ant range
        ant = ants.ShortThrower()
        ant.max_range = 10
        self.colony.places["tunnel_0_0"].add_insect(ant)
        #Place a bee out of normal range
        bee = ants.Bee(2)
        self.colony.places["tunnel_0_6"].add_insect(bee)
        ant.action(self.colony)
        self.assertIs(bee.armor, 1, error_msg)


class TestProblemA6(AntTest):

    def test_wall(self):
        error_msg = "WallAnt isn't parameterized quite right"
        self.assertEqual(4, ants.WallAnt().armor, error_msg)
        self.assertEqual(4, ants.WallAnt.food_cost, error_msg)


class TestProblemA7(AntTest):

    def test_ninja_parameters(self):
        ninja = ants.NinjaAnt()
        self.assertEqual(6, ants.NinjaAnt.food_cost, "NinjaAnt has wrong cost")
        self.assertEqual(1, ninja.armor, "NinjaAnt has wrong armor")

    def test_non_ninja_blocks(self):
        error_msg = "Non-NinjaAnt does not block bees"
        p0 = self.colony.places["tunnel_0_0"]
        p1 = self.colony.places["tunnel_0_1"]
        bee = ants.Bee(2)
        p1.add_insect(bee)
        p1.add_insect(ants.ThrowerAnt())
        bee.action(self.colony)
        self.assertIsNot(p0, bee.place, error_msg)

    def test_ninja_does_not_block(self):
        error_msg = "NinjaAnt blocks bees"
        p0 = self.colony.places["tunnel_0_0"]
        p1 = self.colony.places["tunnel_0_1"]
        bee = ants.Bee(2)
        p1.add_insect(bee)
        p1.add_insect(ants.NinjaAnt())
        bee.action(self.colony)
        self.assertIs(p0, bee.place, error_msg)

    def test_ninja_deadliness(self):
        error_msg = "NinjaAnt does not strike all bees in its place"
        test_place = self.colony.places["tunnel_0_0"]
        for _ in range(3):
            test_place.add_insect(ants.Bee(1))
        ninja = ants.NinjaAnt()
        test_place.add_insect(ninja)
        ninja.action(self.colony)
        self.assertEqual(0, len(test_place.bees), error_msg)

    def test_instance_damage(self):
        error_msg = "Ninja damage not looked up on the instance"
        place = self.colony.places["tunnel_0_0"]
        bee = ants.Bee(900)
        place.add_insect(bee)
        buffNinja = ants.NinjaAnt()
        buffNinja.damage = 500  # Sharpen the sword
        place.add_insect(buffNinja)
        buffNinja.action(self.colony)
        self.assertEqual(400, bee.armor, error_msg)


class TestProblemB6(AntTest):

    def test_scuba_parameters(self):
        scuba = ants.ScubaThrower()
        self.assertEqual(5, ants.ScubaThrower.food_cost, "ScubaThrower has wrong cost")
        self.assertEqual(1, scuba.armor, "ScubaThrower has wrong armor")

    def test_inheritance(self):
        """Tests to see if the ScubaThrower is actually using the inherited
        action from the ThrowerAnt.
        """
        old_thrower_action = ants.ThrowerAnt.action
        def new_thrower_action(self, colony):
            raise NotImplementedError()
        old_throw_at = ants.ThrowerAnt.throw_at
        def new_throw_at(self, target):
            raise NotImplementedError()

        failed_scuba = 0
        try:
            ants.ThrowerAnt.action = new_thrower_action
            test_scuba = ants.ScubaThrower()
            test_scuba.action(self.colony)
        except NotImplementedError:
            failed_scuba += 1
        finally:
            ants.ThrowerAnt.action = old_thrower_action

        try:
            ants.ThrowerAnt.throw_at = new_throw_at
            test_scuba = ants.ScubaThrower()
            test_bee = ants.Bee(1)
            test_scuba.throw_at(test_bee)
        except NotImplementedError:
            failed_scuba += 1
        finally:
            ants.ThrowerAnt.throw_at = old_throw_at

        if failed_scuba < 2:
            self.fail(msg="ScubaThrower is not using inheritance")

    def test_scuba(self):
        error_msg = "ScubaThrower sank"
        water = ants.Water("water")
        ant = ants.ScubaThrower()
        water.add_insect(ant)
        self.assertIs(water, ant.place, error_msg)
        self.assertEqual(1, ant.armor, error_msg)

    def test_scuba_on_land(self):
        place1 = self.colony.places["tunnel_0_0"]
        place2 = self.colony.places["tunnel_0_4"]
        ant = ants.ScubaThrower()
        bee = ants.Bee(3)
        place1.add_insect(ant)
        place2.add_insect(bee)
        ant.action(self.colony)
        self.assertEqual(2, bee.armor, "ScubaThrower doesn't throw on land")

    def test_scuba_in_water(self):
        water = ants.Water("water")
        water.entrance = self.colony.places["tunnel_0_1"]
        target = self.colony.places["tunnel_0_4"]
        ant = ants.ScubaThrower()
        bee = ants.Bee(3)
        water.add_insect(ant)
        target.add_insect(bee)
        ant.action(self.colony)
        self.assertIs(2, bee.armor, "ScubaThrower doesn't throw in water")


class TestProblemB7(AntTest):

    def test_hungry_parameters(self):
        hungry = ants.HungryAnt()
        self.assertEqual(4, ants.HungryAnt.food_cost, "HungryAnt has wrong cost")
        self.assertEqual(1, hungry.armor, "HungryAnt has wrong armor")

    def test_hungry_eats_and_digests(self):
        hungry = ants.HungryAnt()
        super_bee, super_pal = ants.Bee(1000), ants.Bee(1)
        place = self.colony.places["tunnel_0_0"]
        place.add_insect(hungry)
        place.add_insect(super_bee)
        hungry.action(self.colony)
        self.assertEqual(0, super_bee.armor, "HungryAnt didn't eat")
        place.add_insect(super_pal)
        for _ in range(3):
            hungry.action(self.colony)
        self.assertEqual(1, super_pal.armor, "HungryAnt didn't digest")
        hungry.action(self.colony)
        self.assertEqual(0, super_pal.armor, "HungryAnt didn't eat again")

    def test_hungry_waits(self):
        """If you get an IndexError (not an AssertionError) when running
        this test, it"s possible that your HungryAnt is trying to eat a
        bee when no bee is available.
        """
        hungry = ants.HungryAnt()
        place = self.colony.places["tunnel_0_0"]
        place.add_insect(hungry)
        # Wait a few turns before adding Bee
        for _ in range(5):
            hungry.action(self.colony)
        bee = ants.Bee(3)
        place.add_insect(bee)
        hungry.action(self.colony)
        self.assertIs(0, bee.armor, "HungryAnt didn't eat")


    def test_hungry_delay(self):
        # Add very hungry caterpi- um, ant
        very_hungry = ants.HungryAnt()
        very_hungry.time_to_digest = 0
        place = self.colony.places["tunnel_0_0"]
        place.add_insect(very_hungry)
        # Eat all the bees!
        for _ in range(100):
            place.add_insect(ants.Bee(3))
        for _ in range(100):
            very_hungry.action(self.colony)
        self.assertIs(0, len(place.bees),
                      "Digestion time not looked up on the instance")


class TestProblem8(AntTest):

    def setUp(self):
        AntTest.setUp(self)
        self.place = ants.Place("TestProblem8")
        self.bodyguard = ants.BodyguardAnt()
        self.bodyguard2 = ants.BodyguardAnt()
        self.test_ant = ants.Ant()
        self.test_ant2 = ants.Ant()
        self.harvester = ants.HarvesterAnt()

    def test_bodyguard_parameters(self):
        bodyguard = ants.BodyguardAnt()
        self.assertEqual(4, ants.BodyguardAnt.food_cost, "BodyguardAnt has wrong cost")
        self.assertEqual(2, bodyguard.armor, "BodyguardAnt has wrong armor")

    def test_bodyguardant_starts_empty(self):
        error_msg = "BodyguardAnt doesn't start off empty"
        self.assertIsNone(self.bodyguard.ant, error_msg)

    def test_contain_ant(self):
        error_msg = "BodyguardAnt.contain_ant doesn't properly contain ants"
        self.bodyguard.contain_ant(self.test_ant)
        self.assertIs(self.bodyguard.ant, self.test_ant, error_msg)

    def test_bodyguardant_is_container(self):
        error_msg = "BodyguardAnt isn't a container"
        self.assertTrue(self.bodyguard.container, error_msg)

    def test_ant_is_not_container(self):
        error_msg = "Normal Ants are containers"
        self.assertFalse(self.test_ant.container, error_msg)

    def test_can_contain1(self):
        error_msg = "can_contain returns False for container ants"
        self.assertTrue(self.bodyguard.can_contain(self.test_ant), error_msg)

    def test_can_contain2(self):
        error_msg = "can_contain returns True for non-container ants"
        self.assertFalse(self.test_ant.can_contain(self.test_ant2), error_msg)

    def test_can_contain3(self):
        error_msg = "can_contain lets container ants contain other containers"
        self.assertFalse(self.bodyguard.can_contain(self.bodyguard2), error_msg)

    def test_can_contain4(self):
        error_msg = "can_contain lets container ants contain multiple ants"
        self.bodyguard.contain_ant(self.test_ant)
        self.assertFalse(self.bodyguard.can_contain(self.test_ant2), error_msg)

    def test_modified_add_insect1(self):
        error_msg = "Place.add_insect doesn't place Ants on BodyguardAnts properly"
        self.place.add_insect(self.bodyguard)
        try:
            self.place.add_insect(self.test_ant)
        except:
            self.fail(error_msg)
        self.assertIs(self.bodyguard.ant, self.test_ant, error_msg)
        self.assertIs(self.place.ant, self.bodyguard, error_msg)

    def test_modified_add_insect2(self):
        error_msg = \
            "Place.add_insect doesn't place BodyguardAnts on Ants properly"
        self.place.add_insect(self.test_ant)
        try:
            self.place.add_insect(self.bodyguard)
        except:
            self.fail(error_msg)
        self.assertIs(self.bodyguard.ant, self.test_ant, error_msg)
        self.assertIs(self.place.ant, self.bodyguard, error_msg)

    def test_bodyguardant_perish(self):
        error_msg = \
            "BodyguardAnts aren't replaced with the contained Ant when perishing"
        self.place.add_insect(self.bodyguard)
        self.place.add_insect(self.test_ant)
        self.bodyguard.reduce_armor(self.bodyguard.armor)
        self.assertIs(self.place.ant, self.test_ant, error_msg)

    def test_bodyguardant_work(self):
        error_msg = "BodyguardAnts don't let the contained ant do work"
        food = self.colony.food
        self.bodyguard.contain_ant(self.harvester)
        self.bodyguard.action(self.colony)
        self.assertEqual(food+1, self.colony.food, error_msg)

    def test_thrower(self):
        error_msg = "ThrowerAnt can't throw from inside a bodyguard"
        ant = ants.ThrowerAnt()
        self.colony.places["tunnel_0_0"].add_insect(self.bodyguard)
        self.colony.places["tunnel_0_0"].add_insect(ant)
        bee = ants.Bee(2)
        self.colony.places["tunnel_0_3"].add_insect(bee)
        self.bodyguard.action(self.colony)
        self.assertEqual(1, bee.armor, error_msg)

    def test_remove_bodyguard(self):
        error_msg = 'Removing BodyguardAnt also removes containing ant'
        place = self.colony.places['tunnel_0_0']
        bodyguard = ants.BodyguardAnt()
        test_ant = ants.Ant(1)
        place.add_insect(bodyguard)
        place.add_insect(test_ant)
        self.colony.remove_ant('tunnel_0_0')
        self.assertIs(place.ant, test_ant, error_msg)

    def test_bodyguarded_ant_do_action(self):
        error_msg = "Bodyguarded ant does not perform its action"
        class TestAnt(ants.Ant):
            def action(self, colony):
                self.armor += 9000
        test_ant = TestAnt(1)
        place = self.colony.places['tunnel_0_0']
        bodyguard = ants.BodyguardAnt()
        place.add_insect(test_ant)
        place.add_insect(bodyguard)
        place.ant.action(self.colony)
        self.assertEqual(place.ant.ant.armor, 9001, error_msg)

    def test_modified_container(self):
        """Test to see if we can construct a container besides Bodyguard."""
        error_msg = "Container status should not be unique to Bodyguard."
        ant = ants.ThrowerAnt()
        ant.container = True
        ant.ant = None
        self.assertTrue(ant.can_contain(ants.ThrowerAnt()), error_msg)

    def test_modified_guard(self):
        error_msg = "A container should not contain another container."
        bodyguard = ants.BodyguardAnt()
        mod_guard = ants.BodyguardAnt()
        mod_guard.container = False
        self.assertTrue(bodyguard.can_contain(mod_guard), error_msg)


class TestProblem9(AntTest):
    @staticmethod
    def queen_layout(queen, register_place, steps=5):
        "Create a two-tunnel layout with water in the middle of 5 steps."
        for tunnel in range(2):
            exit = queen
            for step in range(steps):
                place = ants.Water if step == steps//2 else ants.Place
                exit = place('tunnel_{0}_{1}'.format(tunnel, step), exit)
                register_place(exit, step == steps-1)

    def setUp(self):
        imp.reload(ants)
        hive = ants.Hive(ants.make_test_assault_plan())
        layout = TestProblem9.queen_layout
        self.colony = ants.AntColony(None, hive, ants.ant_types(), layout)
        self.queen = ants.QueenAnt()
        self.imposter = ants.QueenAnt()

    def test_queen_place(self):
        colony_queen = ants.Place('Original Queen Location of the Colony')
        ant_queen = ants.Place('Place given to the QueenAnt')
        queen_place = ants.QueenPlace(colony_queen, ant_queen)
        colony_queen.bees = [ants.Bee(1, colony_queen) for _ in range(3)]
        ant_queen.bees = [ants.Bee(2, colony_queen) for _ in range(4)]
        self.assertEqual(7, len(queen_place.bees), 'QueenPlace has wrong bees')
        bee_armor = sum(bee.armor for bee in queen_place.bees)
        self.assertEqual(11, bee_armor, 'QueenPlace has wrong bees')

    def test_double(self):
        back = ants.ThrowerAnt()
        thrower_damage = ants.ThrowerAnt.damage
        fire_damage = ants.FireAnt.damage
        front = ants.FireAnt()
        side_back = ants.ThrowerAnt()
        side_front = ants.ThrowerAnt()
        armor, side_armor = 20, 10
        bee, side_bee = ants.Bee(armor), ants.Bee(side_armor)

        self.colony.places['tunnel_0_0'].add_insect(back)
        self.colony.places['tunnel_0_2'].add_insect(self.queen)
        self.colony.places['tunnel_0_4'].add_insect(bee)
        self.colony.places['tunnel_1_1'].add_insect(side_back)
        self.colony.places['tunnel_1_3'].add_insect(side_front)
        self.colony.places['tunnel_1_4'].add_insect(side_bee)

        # Simulate a battle in Tunnel 0 (contains Queen)
        back.action(self.colony)
        armor -= thrower_damage  # No doubling until queen's action
        self.assertEqual(armor, bee.armor, "Damage doubled too early")
        self.queen.action(self.colony)
        armor -= thrower_damage  # Queen should always deal normal damage
        self.assertEqual(armor, bee.armor, "Queen damage incorrect")
        bee.action(self.colony)  # Bee moves forward
        self.colony.places['tunnel_0_3'].add_insect(front)  # Fire ant added
        back.action(self.colony)
        armor -= 2 * thrower_damage  # Damage doubled in back
        self.assertEqual(armor, bee.armor, "Back damage incorrect")
        self.queen.action(self.colony)
        armor -= thrower_damage  # Queen should always deal normal damage
        self.assertEqual(armor, bee.armor, "Queen damage incorrect (2)")
        back.action(self.colony)
        armor -= 2 * thrower_damage  # Thrower damage still doubled
        self.assertEqual(armor, bee.armor, "Back damage incorrect (2)")
        bee.action(self.colony)
        armor -= 2 * fire_damage  # Fire damage doubled
        self.assertEqual(armor, bee.armor, "Fire damage incorrect")

        # Simulate a battle in Tunnel 1 (no Queen)
        self.assertEqual(side_armor, side_bee.armor, "Side bee took damage")
        side_back.action(self.colony)
        side_armor -= thrower_damage  # Ant in another tunnel: normal damage
        self.assertEqual(side_armor, side_bee.armor,
                         "Side back damage incorrect")
        side_front.action(self.colony)
        side_armor -= thrower_damage  # Ant in another tunnel: normal damage
        self.assertEqual(side_armor, side_bee.armor,
                         "Side front damage incorrect")

    def test_die(self):
        bee = ants.Bee(3)
        self.colony.places['tunnel_0_1'].add_insect(self.queen)
        self.colony.places['tunnel_0_2'].add_insect(bee)
        self.queen.action(self.colony)
        self.assertFalse(len(self.colony.queen.bees) > 0, 'Game ended')
        bee.action(self.colony)
        self.assertTrue(len(self.colony.queen.bees) > 0, 'Game not ended')

    def test_imposter(self):
        queen = self.queen
        imposter = self.imposter
        self.colony.places['tunnel_0_0'].add_insect(queen)
        self.colony.places['tunnel_0_1'].add_insect(imposter)
        queen.action(self.colony)
        imposter.action(self.colony)
        self.assertEqual(1, queen.armor, 'Long live the queen')
        self.assertEqual(0, imposter.armor, 'Imposters must die')

    def test_bodyguard(self):
        bee = ants.Bee(3)
        guard = ants.BodyguardAnt()
        guard.damage, doubled = 5, 10
        self.colony.places['tunnel_0_1'].add_insect(self.queen)
        self.colony.places['tunnel_0_1'].add_insect(guard)
        self.colony.places['tunnel_0_2'].add_insect(bee)
        self.queen.action(self.colony)
        self.assertEqual(guard.damage, doubled, 'Bodyguard damage incorrect')
        self.assertFalse(len(self.colony.queen.bees) > 0, 'Game ended')
        bee.action(self.colony)
        self.assertTrue(len(self.colony.queen.bees) > 0, 'Game not ended')

    def test_remove(self):
        queen = self.queen
        imposter = self.imposter
        p0 = self.colony.places['tunnel_0_0']
        p1 = self.colony.places['tunnel_0_1']
        p0.add_insect(queen)
        p1.add_insect(imposter)
        p0.remove_insect(queen)
        p1.remove_insect(imposter)
        self.assertIs(queen, p0.ant, 'Queen removed')
        self.assertIsNone(p1.ant, 'Imposter not removed')
        queen.action(self.colony)

    def test_die_the_old_fashioned_way(self):
        bee = ants.Bee(3)
        queen = self.queen
        # The bee has an uninterrupted path to the heart of the colony
        self.colony.places['tunnel_0_1'].add_insect(bee)
        self.colony.places['tunnel_0_2'].add_insect(queen)
        queen.action(self.colony)
        bee.action(self.colony)
        self.assertFalse(len(self.colony.queen.bees) > 0, 'Game ended')
        queen.action(self.colony)
        bee.action(self.colony)
        self.assertTrue(len(self.colony.queen.bees) > 0, 'Game not ended')

    def test_double_continuous(self):
        """This test makes the queen buff one ant, then the other, to see
        if the queen will continually buff newly added ants.
        """
        self.colony.places['tunnel_0_0'].add_insect(ants.ThrowerAnt())
        self.colony.places['tunnel_0_2'].add_insect(self.queen)
        self.queen.action(self.colony)
        # Add ant and buff
        ant = ants.ThrowerAnt()
        self.colony.places['tunnel_0_1'].add_insect(ant)
        self.queen.action(self.colony)
        # Attack a bee
        bee = ants.Bee(3)
        self.colony.places['tunnel_0_4'].add_insect(bee)
        ant.action(self.colony)
        self.assertEqual(1, bee.armor, "Queen does not buff new ants")


class TestProblemEC(AntTest):

    def test_status_parameters(self):
        slow = ants.SlowThrower()
        stun = ants.StunThrower()
        self.assertEqual(4, ants.SlowThrower.food_cost, "SlowThrower has wrong cost")
        self.assertEqual(6, ants.StunThrower.food_cost, "StunThrower has wrong cost")
        self.assertEqual(1, slow.armor, "SlowThrower has wrong armor")
        self.assertEqual(1, stun.armor, "StunThrower has wrong armor")

    def test_slow(self):
        error_msg = "SlowThrower doesn't cause slowness on odd turns."
        slow = ants.SlowThrower()
        bee = ants.Bee(3)
        self.colony.places["tunnel_0_0"].add_insect(slow)
        self.colony.places["tunnel_0_4"].add_insect(bee)
        slow.action(self.colony)
        self.colony.time = 1
        bee.action(self.colony)
        self.assertEqual("tunnel_0_4", bee.place.name, error_msg)
        self.colony.time += 1
        bee.action(self.colony)
        self.assertEqual("tunnel_0_3", bee.place.name, error_msg)
        for _ in range(3):
            self.colony.time += 1
            bee.action(self.colony)
        self.assertEqual("tunnel_0_1", bee.place.name, error_msg)

    def test_stun(self):
        error_msg = "StunThrower doesn't stun for exactly one turn."
        stun = ants.StunThrower()
        bee = ants.Bee(3)
        self.colony.places["tunnel_0_0"].add_insect(stun)
        self.colony.places["tunnel_0_4"].add_insect(bee)
        stun.action(self.colony)
        bee.action(self.colony)
        self.assertEqual("tunnel_0_4", bee.place.name, error_msg)
        bee.action(self.colony)
        self.assertEqual("tunnel_0_3", bee.place.name, error_msg)

    def test_effect_stack(self):
        stun = ants.StunThrower()
        bee = ants.Bee(3)
        stun_place = self.colony.places["tunnel_0_0"]
        bee_place = self.colony.places["tunnel_0_4"]
        stun_place.add_insect(stun)
        bee_place.add_insect(bee)
        for _ in range(4): # stun bee four times
            stun.action(self.colony)
        for _ in range(4):
            bee.action(self.colony)
            self.assertEqual("tunnel_0_4", bee.place.name,
                             "Status effects do not stack")

    def test_multiple_stuns(self):
        error_msg = "2 StunThrowers stunning 2 Bees doesn't stun each Bee for exactly one turn."
        stun1 = ants.StunThrower()
        stun2 = ants.StunThrower()
        bee1 = ants.Bee(3)
        bee2 = ants.Bee(3)

        self.colony.places["tunnel_0_0"].add_insect(stun1)
        self.colony.places["tunnel_0_1"].add_insect(bee1)
        self.colony.places["tunnel_0_2"].add_insect(stun2)
        self.colony.places["tunnel_0_3"].add_insect(bee2)

        stun1.action(self.colony)
        stun2.action(self.colony)
        bee1.action(self.colony)
        bee2.action(self.colony)

        self.assertEqual("tunnel_0_1", bee1.place.name, error_msg)
        self.assertEqual("tunnel_0_3", bee2.place.name, error_msg)

        bee1.action(self.colony)
        bee2.action(self.colony)

        self.assertEqual("tunnel_0_0", bee1.place.name, error_msg)
        self.assertEqual("tunnel_0_2", bee2.place.name, error_msg)

    def test_long_effect_stack(self):
        stun = ants.StunThrower()
        slow = ants.SlowThrower()
        bee = ants.Bee(3)
        self.colony.places["tunnel_0_0"].add_insect(stun)
        self.colony.places["tunnel_0_1"].add_insect(slow)
        self.colony.places["tunnel_0_4"].add_insect(bee)
        for _ in range(3): # slow bee three times
            slow.action(self.colony)
        stun.action(self.colony) # stun bee once

        self.colony.time = 0
        bee.action(self.colony) # stunned
        self.assertEqual("tunnel_0_4", bee.place.name)

        self.colony.time = 1
        bee.action(self.colony) # slowed thrice
        self.assertEqual("tunnel_0_4", bee.place.name)

        self.colony.time = 2
        bee.action(self.colony) # slowed thrice
        self.assertEqual("tunnel_0_3", bee.place.name)

        self.colony.time = 3
        bee.action(self.colony) # slowed thrice
        self.assertEqual("tunnel_0_3", bee.place.name)

        self.colony.time = 4
        bee.action(self.colony) # slowed twice
        self.assertEqual("tunnel_0_2", bee.place.name)

        self.colony.time = 5
        bee.action(self.colony) # slowed twice
        self.assertEqual("tunnel_0_2", bee.place.name)

        self.colony.time = 6
        bee.action(self.colony) # slowed once
        self.assertEqual("tunnel_0_1", bee.place.name)

        self.colony.time = 7
        bee.action(self.colony) # no effects
        self.assertEqual(0, slow.armor)


project_info = {
    'name': 'Project 3: Ants',
    'remote_index': 'http://inst.eecs.berkeley.edu/~cs61a/fa13/proj/ants/',
    'autograder_files': [
        'ants_grader.py',
    ],
    'version': __version__,
}

@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(description="Run Ants Tests")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--question", '-q')
    args = parser.parse_args()

    autograder.check_for_updates(
        project_info['remote_index'],
        project_info['autograder_files'],
        project_info['version'],
    )

    doctest.testmod(ants, verbose=args.verbose)

    question = args.question
    if question:
        question = question.upper()
        test_name = 'TestProblem' + question
        if test_name in globals():
            test = globals()[test_name]
            suite = unittest.makeSuite(test)
            runner = unittest.TextTestRunner()
        else:
            print('Question "{0}" not recognized.'.format(args.question),
                  'Try one of the following instead:')
            print('  2  3  A4  A5  B4  B5  A6  A7  B6  B7  8  9  EC')
            return

    stdout = sys.stdout # suppressing print statements from ants.py
    with open(os.devnull, "w") as sys.stdout:
        verbosity = 2 if args.verbose else 1
        if question:
            runner.run(suite)
        else:
            tests = unittest.main(exit=False, verbosity=verbosity)
    sys.stdout = stdout
