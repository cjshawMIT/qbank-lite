# -*- coding: utf-8 -*-

import os
import json

from dlkit_runtime.primitives import Type

from records.registry import ITEM_GENUS_TYPES, QUESTION_GENUS_TYPES, ANSWER_GENUS_TYPES

from testing_utilities import BaseTestCase

from urllib import unquote


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ABS_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

DRAG_AND_DROP_ITEM_GENUS_TYPE = Type(**ITEM_GENUS_TYPES['drag-and-drop'])
DRAG_AND_DROP_QUESTION_GENUS_TYPE = Type(**QUESTION_GENUS_TYPES['drag-and-drop'])
WRONG_ANSWER = Type(**ANSWER_GENUS_TYPES['wrong-answer'])
RIGHT_ANSWER = Type(**ANSWER_GENUS_TYPES['right-answer'])

SNAP_DROP_BEHAVIOR = 'drop.behavior%3Asnap%40ODL.MIT.EDU'
DROP_DROP_BEHAVIOR = 'drop.behavior%3Adrop%40ODL.MIT.EDU'
REJECT_DROP_BEHAVIOR = 'drop.behavior%3Areject%40ODL.MIT.EDU'


class BaseDragAndDropTestCase(BaseTestCase):
    @staticmethod
    def _item_payload():
        """payload without the question and answer parts.
        Pull in self._question_payload() and self._answers_payload() if you need those"""
        return {
            'genusTypeId': str(DRAG_AND_DROP_ITEM_GENUS_TYPE),
            'name': 'Test drag and drop item'
        }

    def _question_payload(self):
        payload = {
            'targets': [{
                'text': '<p><img src="AssetContent:drag_and_drop_input_DPP-Concpt-BlkonRmp-Trgt_png" /></p>',
                'name': 'Image of ramp',
                'dropBehaviorType': REJECT_DROP_BEHAVIOR
            }],
            'droppables': [{
                'text': '<p><img src="AssetContent:draggable_green_dot_png" /></p>',
                'name': 'Green dot',
                'reuse': 1,
                'dropBehaviorType': DROP_DROP_BEHAVIOR
            }, {
                'text': '<p><img src="AssetContent:draggable_red_dot_png" /></p>',
                'name': 'Red dot',
                'reuse': 4,
                'dropBehaviorType': DROP_DROP_BEHAVIOR
            }],
            'zones': [{
                'spatialUnit': {
                    'recordType': 'osid.mapping.SpatialUnit%3Arectangle%40ODL.MIT.EDU',
                    'coordinate': [0, 0],
                    'width': 50,
                    'height': 30
                },
                'containerId': 0,
                'dropBehaviorType': SNAP_DROP_BEHAVIOR,
                'name': u'Zone Á',
                'reuse': 0,
                'visible': False
            }, {
                'spatialUnit': {
                    'recordType': 'osid.mapping.SpatialUnit%3Arectangle%40ODL.MIT.EDU',
                    'coordinate': [100, 100],
                    'width': 30,
                    'height': 50
                },
                'containerId': 0,
                'dropBehaviorType': DROP_DROP_BEHAVIOR,
                'name': u'जोन बी',
                'reuse': 2,
                'visible': True
            }],
            'fileIds': {},
            'genusTypeId': str(DRAG_AND_DROP_QUESTION_GENUS_TYPE),
            'shuffleDroppables': True,
            'shuffleTargets': False,
            'shuffleZones': True
        }

        media_files = [self._target,
                       self._draggable1,
                       self._draggable2]

        assets = {}
        for media_file in media_files:
            label = self._label(self._filename(media_file))
            assets[label] = self.upload_media_file(media_file)

        for label, asset in assets.iteritems():
            payload['fileIds'][label] = {}
            payload['fileIds'][label]['assetId'] = asset['id']
            payload['fileIds'][label]['assetContentId'] = asset['assetContents'][0]['id']
            payload['fileIds'][label]['assetContentTypeId'] = asset['assetContents'][0]['genusTypeId']

        return payload

    def _answers_payload(self):
        payload = [{
            'feedback': '<p>Good job! <audio type="audio/mp3"><source src="AssetContent:audio_feedback_mp3" /></audio></p>',
            'zoneConditions': [{
                'zoneId': 0,
                'droppableId': 0
            }, {
                'zoneId': 1,
                'droppableId': 1
            }],
            'fileIds': {},
            'genusTypeId': str(RIGHT_ANSWER)
        }, {
            'feedback': '<p>Try again! <audio type="audio/mp3"><source src="AssetContent:audio_feedback_mp3" /></audio></p>',
            'zoneConditions': [{
                'zoneId': 0,
                'droppableId': 1
            }, {
                'zoneId': 1,
                'droppableId': 0
            }],
            'fileIds': {},
            'genusTypeId': str(WRONG_ANSWER)
        }]

        media_files = [self._audio_feedback]

        assets = {}
        for media_file in media_files:
            label = self._label(self._filename(media_file))
            assets[label] = self.upload_media_file(media_file)

        for label, asset in assets.iteritems():
            payload[0]['fileIds'][label] = {}
            payload[0]['fileIds'][label]['assetId'] = asset['id']
            payload[0]['fileIds'][label]['assetContentId'] = asset['assetContents'][0]['id']
            payload[0]['fileIds'][label]['assetContentTypeId'] = asset['assetContents'][0]['genusTypeId']

            payload[1]['fileIds'][label] = {}
            payload[1]['fileIds'][label]['assetId'] = asset['id']
            payload[1]['fileIds'][label]['assetContentId'] = asset['assetContents'][0]['id']
            payload[1]['fileIds'][label]['assetContentTypeId'] = asset['assetContents'][0]['genusTypeId']

        return payload

    def create_item_without_question_or_answers(self):
        pass

    def create_item_with_question_and_answers(self):
        pass

    def setUp(self):
        self._target = open('{0}/tests/files/drag-and-drop/drag_and_drop_input_DPP-Concpt-BlkonRmp-Trgt.png'.format(ABS_PATH), 'rb')
        self._draggable1 = open('{0}/tests/files/drag-and-drop/draggable_green_dot.png'.format(ABS_PATH), 'rb')
        self._draggable2 = open('{0}/tests/files/drag-and-drop/draggable_red_dot.png'.format(ABS_PATH), 'rb')
        self._audio_feedback = open('{0}/tests/files/audio_feedback.mp3'.format(ABS_PATH), 'rb')

        super(BaseDragAndDropTestCase, self).setUp()
        self.url = '/api/v1/assessment/banks/{0}/items'.format(unquote(str(self._bank.ident)))

    def tearDown(self):
        super(BaseDragAndDropTestCase, self).tearDown()
        self._target.close()
        self._draggable1.close()
        self._draggable2.close()
        self._audio_feedback.close()


class CreateTests(BaseDragAndDropTestCase):
    """Can create drag and drop RESTfully"""
    def test_can_create_item_with_question_and_answers(self):
        """Make sure question genusTypeId is set properly"""
        payload = self._item_payload()
        payload['question'] = self._question_payload()
        payload['answers'] = self._answers_payload()

        req = self.app.post(self.url,
                            params=json.dumps(payload),
                            headers={'content-type': 'application/json'})
        self.ok(req)
        data = self.json(req)
        question = data['question']
        self.assertEqual(data['genusTypeId'], str(DRAG_AND_DROP_ITEM_GENUS_TYPE))
        self.assertEqual(question['genusTypeId'], str(DRAG_AND_DROP_QUESTION_GENUS_TYPE))

        # check the three shuffle flags in the question match the payload
        self.assertEqual(question['shuffleDroppables'],
                         payload['question']['shuffleDroppables'])
        self.assertEqual(question['shuffleTargets'],
                         payload['question']['shuffleTargets'])
        self.assertEqual(question['shuffleZones'],
                         payload['question']['shuffleZones'])

        # make sure the media files all show as URLs
        self.assertIn('fileIds', question)
        for droppable in question['droppables']:
            self.assertIn('/api/v1/repository/repositories', droppable['text'])
            self.assertIn('/stream', droppable['text'])
        for target in question['targets']:
            self.assertIn('/api/v1/repository/repositories', target['text'])
            self.assertIn('/stream', target['text'])
        for answer in data['answers']:
            self.assertIn('/api/v1/repository/repositories', answer['feedback']['text'])
            self.assertIn('/stream', answer['feedback']['text'])
            self.assertIn('fileIds', answer)

        # make sure droppables, targets, and zones appear
        self.assertEqual(len(question['droppables']),
                         len(payload['question']['droppables']))
        self.assertEqual(len(question['targets']),
                         len(payload['question']['targets']))
        self.assertEqual(len(question['zones']),
                         len(payload['question']['zones']))

        # check that the various arguments are saved correctly for the question
        # i.e. visible, reuse, name, etc.
        # use the multiLanguage versions to check, since those aren't shuffled
        # and we can index-match to the payload easier
        for index, droppable in enumerate(question['multiLanguageDroppables']):
            self.assertEqual(droppable['name'],
                             payload['question']['droppables'][index]['name'])
            self.assertEqual(droppable['reuse'],
                             payload['question']['droppables'][index]['reuse'])
            self.assertEqual(droppable['dropBehaviorType'],
                             payload['question']['droppables'][index]['dropBehaviorType'])
        for index, target in enumerate(question['multiLanguageTargets']):
            self.assertEqual(target['name'],
                             payload['question']['targets'][index]['name'])
            self.assertEqual(target['dropBehaviorType'],
                             payload['question']['targets'][index]['dropBehaviorType'])
        for index, zone in enumerate(question['multiLanguageZones']):
            self.assertEqual(zone['reuse'],
                             payload['question']['zones'][index]['reuse'])
            self.assertEqual(zone['dropBehaviorType'],
                             payload['question']['zones'][index]['dropBehaviorType'])
            self.assertEqual(zone['visible'],
                             payload['question']['zones'][index]['visible'])
            self.assertEqual(zone['spatialUnit']['width'],
                             payload['question']['zones'][index]['spatialUnit']['width'])
            self.assertEqual(zone['spatialUnit']['height'],
                             payload['question']['zones'][index]['spatialUnit']['height'])
            self.assertEqual(zone['spatialUnit']['coordinateValues'],
                             payload['question']['zones'][index]['spatialUnit']['coordinate'])
            self.assertEqual(zone['spatialUnit']['recordTypes'][0],
                             payload['question']['zones'][index]['spatialUnit']['recordType'])

        # make sure the multi-language stuff comes out right in the question object_map
        self.assertIn('multiLanguageDroppables', question)
        for droppable in question['multiLanguageDroppables']:
            self.assertNotIn('text', droppable)
            self.assertIn('texts', droppable)
        for droppable in question['droppables']:
            self.assertIn('text', droppable)
            self.assertNotIn('texts', droppable)
        self.assertIn('multiLanguageTargets', question)
        for target in question['multiLanguageTargets']:
            self.assertNotIn('text', target)
            self.assertIn('texts', target)
        for target in question['targets']:
            self.assertIn('text', target)
            self.assertNotIn('texts', target)
        self.assertIn('multiLanguageZones', question)
        for zone in question['multiLanguageZones']:
            self.assertNotIn('name', zone)
            self.assertIn('names', zone)
        for zone in question['zones']:
            self.assertIn('name', zone)
            self.assertNotIn('names', zone)

        # check the answers
        self.assertEqual(len(data['answers']), 2)
        self.assertEqual(data['answers'][0]['genusTypeId'], str(RIGHT_ANSWER))
        self.assertEqual(data['answers'][1]['genusTypeId'], str(WRONG_ANSWER))
        for answer in data['answers']:
            self.assertEqual(len(answer['spatialUnitConditions']), 0)
            self.assertEqual(len(answer['coordinateConditions']), 0)
            self.assertEqual(len(answer['zoneConditions']), 2)

        # check that the indices all got converted to the right IDs for question zones
        # and answer zone conditions
        # Especially important with the shuffling!
        expected_target_id = question['targets'][0]['id']
        for zone in question['zones']:
            self.assertEqual(zone['containerId'], expected_target_id)

        expected_droppable_0_id = question['multiLanguageDroppables'][0]['id']
        expected_droppable_1_id = question['multiLanguageDroppables'][1]['id']

        expected_zone_0_id = question['multiLanguageZones'][0]['id']
        expected_zone_1_id = question['multiLanguageZones'][1]['id']
        for answer in data['answers']:
            if answer['genusTypeId'] == str(RIGHT_ANSWER):
                for zone_condition in answer['zoneConditions']:
                    if zone_condition['droppableId'] == expected_droppable_0_id:
                        self.assertEqual(zone_condition['zoneId'],
                                         expected_zone_0_id)
                    else:
                        self.assertEqual(zone_condition['droppableId'],
                                         expected_droppable_1_id)
                        self.assertEqual(zone_condition['zoneId'],
                                         expected_zone_1_id)
            else:
                for zone_condition in answer['zoneConditions']:
                    if zone_condition['droppableId'] == expected_droppable_1_id:
                        self.assertEqual(zone_condition['zoneId'],
                                         expected_zone_0_id)
                    else:
                        self.assertEqual(zone_condition['droppableId'],
                                         expected_droppable_0_id)
                        self.assertEqual(zone_condition['zoneId'],
                                         expected_zone_1_id)

    def test_can_create_item_without_question_or_answers(self):
        payload = self._item_payload()

        req = self.app.post(self.url,
                            params=json.dumps(payload),
                            headers={'content-type': 'application/json'})
        self.ok(req)
        data = self.json(req)
        self.assertEqual(data['genusTypeId'], str(DRAG_AND_DROP_ITEM_GENUS_TYPE))

    def test_shuffled_droppables_do_not_shuffle_for_authoring(self):
        payload = self._item_payload()
        payload['question'] = self._question_payload()
        payload['answers'] = self._answers_payload()

        req = self.app.post(self.url,
                            params=json.dumps(payload),
                            headers={'content-type': 'application/json'})
        self.ok(req)
        data = self.json(req)
        self.assertTrue(data['question']['shuffleDroppables'])
        original_droppable_ids_order = [d['id'] for d in data['question']['multiLanguageDroppables']]

        num_different = 0

        item_url = '{0}/{1}'.format(self.url,
                                    data['id'])

        for i in range(0, 15):
            req2 = self.app.get(item_url)
            self.ok(req)
            data2 = self.json(req2)
            droppable_ids_order_2 = [d['id'] for d in data2['question']['droppables']]

            if original_droppable_ids_order != droppable_ids_order_2:
                num_different += 1
        self.assertTrue(num_different == 0)

    def test_shuffled_targets_do_not_shuffle_for_authoring(self):
        self.fail('finish writing the test')

    def test_shuffled_zones_do_not_shuffle_for_authoring(self):
        self.fail('finish writing hte test')

    def test_still_creates_question_if_target_source_tag_not_in_file_ids(self):
        self.fail('finish writing the test')

    def test_still_creates_question_if_droppable_source_tag_not_in_file_ids(self):
        self.fail('finish writing the test')

    def test_cannot_set_zone_to_negative_target_index(self):
        self.fail('finish writing the test')

    def test_cannot_set_zone_to_non_existent_target_index(self):
        self.fail('finish writing the test')

    def test_cannot_set_answer_droppable_to_negative_index(self):
        self.fail('finish writing the test')

    def test_cannot_set_answer_droppable_to_non_existent_index(self):
        self.fail('finish writing the test')

    def test_cannot_set_answer_zone_to_negative_index(self):
        self.fail('finish writing the test')

    def test_cannot_set_answer_zone_to_non_existent_index(self):
        self.fail('finish writing the test')


class UpdateTests(BaseDragAndDropTestCase):
    """Can edit the drag and drop RESTfully"""
    def test_can_add_question_to_existing_item(self):
        self.fail('finish writing the test')

    def test_can_add_answers_to_existing_item(self):
        self.fail('finish writing the test')

    def test_can_update_zone_with_new_language(self):
        self.fail('finish writing the test')

    def test_can_remove_zone_language(self):
        self.fail('finish writing the test')

    def test_can_add_new_zone(self):
        self.fail('finish writing the test')

    def test_can_clear_zone_names(self):
        self.fail('finish writing the test')

    def test_can_change_zone_visibility(self):
        self.fail('finish writign the test')

    def test_can_change_zone_reuse(self):
        self.fail('finish writing the test')

    def test_can_change_zone_drop_behavior(self):
        self.fail('finish writing the test')

    def test_can_change_zone_spatial_unit(self):
        self.fail('finish writing the test')

    def test_can_change_zone_container(self):
        self.fail('finish writing the test')

    def test_can_update_target_with_new_language(self):
        self.fail('finish writing the test')

    def test_can_remove_target_language(self):
        self.fail('finish writing the test')

    def test_can_add_new_target(self):
        self.fail('finish writing the test')

    def test_can_clear_target_texts(self):
        self.fail('finish writing the test')

    def test_can_change_target_name(self):
        self.fail("finish writing the test")

    def test_can_change_target_drop_behavior(self):
        self.fail('finish writign the test')

    def test_can_update_droppable_with_new_language(self):
        self.fail('finish writing the test')

    def test_can_remove_droppable_language(self):
        self.fail('finish writing the test')

    def test_can_add_new_droppable(self):
        self.fail('finish writing the test')

    def test_can_clear_droppable_texts(self):
        self.fail('finish writing the test')

    def test_can_change_droppable_reuse(self):
        self.fail('finish writing hte test')

    def test_can_add_new_file_to_question(self):
        self.fail('finish writing the test')

    def test_can_turn_shuffle_droppables_off(self):
        self.fail('finish writing the test')

    def test_can_turn_shuffle_droppables_on(self):
        self.fail('finish writing the test')

    def test_can_turn_shuffle_targets_on(self):
        self.fail('finish writing the test')

    def test_can_turn_shuffle_targets_off(self):
        self.fail('finish writing the test')

    def test_can_turn_shuffle_zones_on(self):
        self.fail('finish writing the test')

    def test_can_turn_shuffle_zones_off(self):
        self.fail('finish writing the test')

    def test_can_set_targets_order(self):
        self.fail('finish writing the test')

    def test_can_set_droppables_order(self):
        self.fail('finish writing the test')

    def test_can_set_zone_order(self):
        self.fail('finish writing the test')


class DeleteTests(BaseDragAndDropTestCase):
    """Can delete various parts RESTfully"""
    def test_can_delete_drag_and_drop_item(self):
        self.fail('finish writing the test')

    def test_can_remove_droppable(self):
        self.fail('finish writing the test')

    def test_can_remove_target(self):
        self.fail('finish writing the test')

    def test_can_remove_zone(self):
        self.fail('finish writing the test')

    def test_can_remove_answer(self):
        self.fail('finish writing the test')


class QTITests(BaseDragAndDropTestCase):
    def test_xml_includes_targets_zones_and_droppables(self):
        self.fail('finish writing the test')

    def test_xml_returned_even_if_droppable_source_not_in_file_ids(self):
        self.fail('finsih writing the test')

    def test_xml_returned_even_if_target_source_not_in_file_ids(self):
        self.fail('finish writing the test')


class SingleTargetTakingTests(BaseDragAndDropTestCase):
    """Can submit right / wrong answers to a drag-and-drop question"""
    def test_shuffled_droppables_do_shuffle_when_taking(self):
        self.fail('finish writing the test')

    def test_shuffled_targets_do_shuffle_when_taking(self):
        self.fail('finish writing the test')

    def test_can_submit_wrong_answer(self):
        self.fail('finish writing the test')

    def test_can_submit_right_answer(self):
        self.fail('finish writing the test')

    def test_can_submit_coordinate_off_of_the_target(self):
        self.fail('finish writing the test')

    def test_can_submit_negative_coordinates(self):
        self.fail('finish writing the test')

    def test_can_submit_coordinate_on_the_zone_boundary(self):
        self.fail('finish writing the test')

    def test_text_comes_back_in_desired_language(self):
        """ Check that zones, targets, and droppables all return the right language
        """
        self.fail('finish writing the test')

    def test_image_urls_come_back_in_targets(self):
        self.fail('finish writing the test')

    def test_image_urls_come_back_in_droppables(self):
        self.fail('finish writing the test')
