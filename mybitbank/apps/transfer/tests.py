import StringIO
import io

from mybitbank.libs.misc.stubconnector import ServiceProxyStubBTC, ServiceProxyStubBTCWithPass
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.test.utils import setup_test_environment
from lxml import etree

from mybitbank.libs.connections import connector

'''
rawData = {
           'passphrase': 'testpassphrase',
           'new_account_address': "new account address",
           'accounts': {
                        u'': Decimal('0.00000000'),
                        u'pipes': Decimal('0E-8'),
                        u'another account': Decimal('0E-8'),
                        u'my empty account': Decimal('0E-8'),
                        u'my test BTC account': Decimal('230.00000000'),
                        u'sdfsdfs': Decimal('0E-8')
                        },
           
           'addresses': {
                       u'': ['address for default account'],
                       u'pipes': ['address for pipes account', 'second address for pipes account'],
                       u'another account': ['mxgWFbqGPywQUKNXdAd3G2EH6Te1Kag5MP'],
                       u'my empty account': ['address for empty account'],
                       u'my test BTC account': ['mox7nxwfu9hrTQCn24RBTDce1wiHEP1NQp'],
                       u'sdfsdfs': ['address for sdfsdfs account'],
                       },
           'transactions': {
                           u'': [{
                                    "account" : "",
                                    "address" : "address for default account",
                                    "category" : "receive",
                                    "amount" : 15.60073559,
                                    "confirmations" : 5944,
                                    "blockhash" : "0000000000000009b4bec9a4374031762c7c9700eab2a9442336712fc769d7e7",
                                    "blockindex" : 427,
                                    "blocktime" : 1379839630,
                                    "txid" : "9599c2c44e1be0001ad8c03038b50b47e634329917eb6d08f7fc675310075f02",
                                    "time" : 1379839327,
                                    "timereceived" : 1379839327
                                }],
                           u'pipes':  [{
                                            "account" : "pipes",
                                            "address" : "address for pipes account",
                                            "category" : "receive",
                                            "amount" : 12.20073359,
                                            "confirmations" : 5944,
                                            "blockhash" : "0000000000000009b4bec9a4374031762c7c9700eab2a9442336712fc769d7e7",
                                            "blockindex" : 427,
                                            "blocktime" : 1379839630,
                                            "txid" : "9599c2c44e1be0001ad8c03038b50b47e634329917eb6d08f7fc675310075f02",
                                            "time" : 1379839327,
                                            "timereceived" : 1379839327
                                        },
                                       {
                                            "account" : "pipes",
                                            "address" : "address for pipes account",
                                            "category" : "receive",
                                            "amount" : 1.245,
                                            "confirmations" : 345,
                                            "blockhash" : "0000000000000009b4bec9a4374031762c7c9700eab2a9442336712fc769d7e7",
                                            "blockindex" : 427,
                                            "blocktime" : 1379836630,
                                            "txid" : "9599c2c44e1be0001ad8c03038b50b47e634329917eb6d08f7fc675310075f02",
                                            "time" : 1372339327,
                                            "timereceived" : 1379839327
                                        }],
                           u'another account': [],
                           u'my empty account': [],
                           u'my test BTC account': [{
                                                        "account" : "",
                                                        "address" : "address for default account",
                                                        "category" : "receive",
                                                        "amount" : 15.60073559,
                                                        "confirmations" : 5944,
                                                        "blockhash" : "0000000000000009b4bec9a4374031762c7c9700eab2a9442336712fc769d7e7",
                                                        "blockindex" : 427,
                                                        "blocktime" : 1379839630,
                                                        "txid" : "9599c2c44e1be0001ad8c03038b50b47e634329917eb6d08f7fc675310075f02",
                                                        "time" : 1379839327,
                                                        "timereceived" : 1379839327
                                                    }],
                           u'sdfsdfs': [],
                        },
                  'balance': Decimal('30.00000000'),
                  
                  
                  'rawtransactions':  [
                                                {   u'blockhash': u'00000000f623a840f81762114d5426faabeb2fcf8b13e3edb128273aa24a3c38',
                                                        u'blocktime': 1382465670,
                                                        u'confirmations': 73,
                                                        u'hex': u'01000000018419d61304f827e0743e84ce3ae694ac2adbc43ca57c5c8997543eba1b8b9fa4000000006a4730440220475a95f43295daaf6575ee0cd9e576d6d6f95a25e7ca51950f9976f4570f294302206798592cfa435be24e503325b0a11364d61ec0c5aab494049b5d35208ed24edf012103d0b8349514469b2c42b41f2aa8982d4b9a666c1662865bd4728c04ad535739f4ffffffff0260d0bb27000000001976a9146608824a44bf9d4c4c7440227143f9b8283439b388ac9002cc00000000001976a914bc488f1667ee3e8b42bb95e320341689f0c5ffc788ac00000000',
                                                        u'locktime': 0,
                                                        u'time': 1382465670,
                                                        u'txid': u'd1f51c53cc35e14596a6cd3607689927dd1ef0d133037883b7dd85f058ffab73',
                                                        u'version': 1,
                                                        u'vin': [   {   u'scriptSig': {   u'asm': u'30440220475a95f43295daaf6575ee0cd9e576d6d6f95a25e7ca51950f9976f4570f294302206798592cfa435be24e503325b0a11364d61ec0c5aab494049b5d35208ed24edf01 03d0b8349514469b2c42b41f2aa8982d4b9a666c1662865bd4728c04ad535739f4',
                                                                                          u'hex': u'4730440220475a95f43295daaf6575ee0cd9e576d6d6f95a25e7ca51950f9976f4570f294302206798592cfa435be24e503325b0a11364d61ec0c5aab494049b5d35208ed24edf012103d0b8349514469b2c42b41f2aa8982d4b9a666c1662865bd4728c04ad535739f4'},
                                                                        u'sequence': 4294967295,
                                                                        u'txid': u'a49f8b1bba3e5497895c7ca53cc4db2aac94e63ace843e74e027f80413d61984',
                                                                        u'vout': 0}],
                                                        u'vout': [   {   u'n': 0,
                                                                         u'scriptPubKey': {   u'addresses': [   u'mppTQqFFXmk2E4F1FJ5A2BqDt56oYH2Nss'],
                                                                                              u'asm': u'OP_DUP OP_HASH160 6608824a44bf9d4c4c7440227143f9b8283439b3 OP_EQUALVERIFY OP_CHECKSIG',
                                                                                              u'hex': u'76a9146608824a44bf9d4c4c7440227143f9b8283439b388ac',
                                                                                              u'reqSigs': 1,
                                                                                              u'type': u'pubkeyhash'},
                                                                         u'value': Decimal('6.66620000')},
                                                                     {   u'n': 1,
                                                                         u'scriptPubKey': {   u'addresses': [   u'mxgWFbqGPywQUKNXdAd3G2EH6Te1Kag5MP'],
                                                                                              u'asm': u'OP_DUP OP_HASH160 bc488f1667ee3e8b42bb95e320341689f0c5ffc7 OP_EQUALVERIFY OP_CHECKSIG',
                                                                                              u'hex': u'76a914bc488f1667ee3e8b42bb95e320341689f0c5ffc788ac',
                                                                                              u'reqSigs': 1,
                                                                                              u'type': u'pubkeyhash'},
                                                                         u'value': Decimal('0.13370000')}]}
                                                
                                                ]
                                      
           }

class ServiceProxyStubBTC(object):
    def __init__(self):
        self._rawData = rawData
        
    def listaccounts(self):
        return self._rawData['accounts']

    def getaddressesbyaccount(self, account_name):
        try:
            return self._rawData['addresses'][account_name]
        except:
            return False
        
    def listtransactions(self, account_name, count=10, start=0):
        return self._rawData['transactions'][account_name]

    def getnewaddress(self, account_name):
        return self._rawData['new_account_address']
    
    def getbalance(self):
        return self._rawData['balance']
    
    def move(self, from_account, to_account, amount, minconf, comment):
        return True
    
    def sendfrom(self, from_account, to_address, amount, minconf, comment, comment_to):
        return True

    def walletpassphrase(self, passphrase, timeout):
        return True
    
    def walletlock(self):
        return True
    
    def getrawtransaction(self, txid, verbose=1):
        return self._rawData['rawtransaction'][0]

'''

class TransferIndexTests(TestCase):
    def setUp(self):
        setup_test_environment()
        connector.services = {1: ServiceProxyStubBTC()}
        connector.config = {1: {'id': int(1),
                             'rpcusername': "testuser",
                             'rpcpassword': "testnet",
                             'rpchost': "localhost",
                             'rpcport': "7000",
                             'name': 'Bitcoin (BTC)',
                             'currency': 'btc',
                             'symbol': "B",
                             'code': 'BTC',
                             'network': "testnet",
                             'enabled': True,
                           }, }
            
        connector.alerts = {}
        
        user = User.objects.create_user('testing', 'testing@testingpipes.com', 'testingpassword')
        user.save()

    def stripHeaders(self, response):
        '''
        String the HTTP headers of the response
        '''
        html_response = ""
        line_no = 0
        io_response = io.BytesIO(str(response))
        for i, line in enumerate(io_response, 1):
            if "DOCTYPE" in line:
                line_no = i
                
        io_response.seek(0)
        with io_response as f:
            html_list = f.readlines()[(line_no - 1):]

        return html_response.join(html_list)

    def validateHTML(self, html):
        try:
            parser = etree.HTMLParser(recover=True)
            tree = etree.parse(StringIO.StringIO(html), parser)
            return tree
        except:
            raise
            return False

    def test_index_account_menus(self):
        '''
        Test if there are accounts in the dropdownmenus
        '''
        
        client = Client()
        client.login(username='testing', password='testingpassword')
        response = client.get(reverse('transfer:index'))
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)
        
        from_account_options = html_tree.xpath("//select[@id='from_account']/option")
        to_account_options = html_tree.xpath("//select[@id='to_account']/option")

        self.assertEquals(len(from_account_options), 7)
        self.assertEquals(len(to_account_options), 7)
        
    def test_tranfer_submit_XSRF_failure(self):
        '''
        Test XSRF errors come out an empty POST
        '''
        
        provider_id = 1
        client = Client(enforce_csrf_checks=True)
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': "",
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "",
                    'provider_id': provider_id,
                    'to_address': ""
                    }
        
        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        
        self.assertContains(response, '403', status_code=403)
        
    def test_tranfer_submit_empty_values(self):
        '''
        Test empty form submittion
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': "",
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "",
                    'provider_id': provider_id,
                    'to_address': ""
                    }
        
        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)
        
        self.assertNotEquals(html_tree.xpath('//*[@id="error_message_from_account"]'), []) 
        self.assertNotEquals(html_tree.xpath('//*[@id="error_message_to_address"]'), [])
        self.assertNotEquals(html_tree.xpath('//*[@id="error_message_amount"]'), [])
        
    def test_tranfer_submit_with_from_account_value(self):
        '''
        Test with from address value only
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': "",
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "mox7nxwfu9hrTQCn24RBTDce1wiHEP1NQp",
                    'provider_id': provider_id,
                    'to_address': ""
                    }
        
        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)
        
        self.assertEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[2]/div/div/ul[@class='errorlist']"), []) 
        self.assertNotEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[3]/div/div/ul[@class='errorlist']"), [])
        self.assertNotEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[6]/div/div/ul[@class='errorlist']"), [])
       
    def test_tranfer_submit_with_to_account_value(self):
        '''
        Test with to address value only
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': "",
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "",
                    'provider_id': 1,
                    'to_address': "mox7nxwfu9hrTQCn24RBTDce1wiHEP1NQp"
                    }
        
        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)
        
        self.assertNotEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[2]/div/div/ul[@class='errorlist']"), []) 
        self.assertEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[3]/div/div/ul[@class='errorlist']"), [])
        self.assertNotEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[6]/div/div/ul[@class='errorlist']"), []) 
        
    def test_tranfer_submit_with_from_to_values(self):
        '''
        Test with from/to addresses without amount
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': "",
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "mxgWFbqGPywQUKNXdAd3G2EH6Te1Kag5MP",
                    'provider_id': provider_id,
                    'to_address': "mox7nxwfu9hrTQCn24RBTDce1wiHEP1NQp"
                    }
        
        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)
        
        self.assertEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[2]/div/div/ul[@class='errorlist']"), []) 
        self.assertEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[3]/div/div/ul[@class='errorlist']"), [])
        self.assertNotEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[6]/div/div/ul[@class='errorlist']"), []) 
        
    def test_tranfer_submit_with_from_to_same_values(self):
        '''
        Test same address for from and to
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': "",
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "mxgWFbqGPywQUKNXdAd3G2EH6Te1Kag5MP",
                    'selected_currency': "btc",
                    'to_address': "mxgWFbqGPywQUKNXdAd3G2EH6Te1Kag5MP"
                    }
        
        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)
        
        self.assertNotEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[2]/strong/ul[@class='errorlist']"), []) 
        
    def test_tranfer_submit_with_correct_values_move(self):
        '''
        Test correct value -> move
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': 3,
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "mxgWFbqGPywQUKNXdAd3G2EH6Te1Kag5MP",
                    'provider_id': provider_id,
                    'to_address': "mox7nxwfu9hrTQCn24RBTDce1wiHEP1NQp"
                    }
        
        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        self.assertContains(response, text='', count=None, status_code=302)
        
    def test_tranfer_submit_test_invalid_provider_id(self):
        '''
        Test invalid provider_id
        '''
        
        provider_id = 9
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': 3,
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "mxgWFbqGPywQUKNXdAd3G2EH6Te1Kag5MP",
                    'provider_id': provider_id,
                    'to_address': "mox7nxwfu9hrTQCn24RBTDce1wiHEP1NQp"
                    }

        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)
        self.assertNotEquals(html_tree.xpath("/html/body/div/form/div/div[2]/div[2]/strong/ul[@class='errorlist']"), [])
    
    def test_tranfer_submit_invalid_address(self):
        '''
        Test invalid address
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        post_data = {
                    'amount': 3,
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_address': "mxgWFbqGPywQUK",
                    'provider_id': provider_id,
                    'to_address': "mox7nxwfu9hrTQCn24RBTDce"
                    }

        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)

        # validate HTML
        self.assertNotEquals(html_tree, False)

        self.assertNotEquals(html_tree.xpath('//*[@id="error_message_to_address"]'), [])
        
    def test_tranfer_submit_required_pass(self):
        '''
        Test invalid address
        '''
        
        provider_id = 1
        client = Client()
        client.login(username='testing', password='testingpassword')
        
        connector.services = {provider_id: ServiceProxyStubBTCWithPass()}
        
        post_data = {
                    'amount': 3,
                    'comment': "",
                    'comment_to': "",
                    'csrfmiddlewaretoken': "",
                    'from_account': "my test BTC account",
                    'provider_id': provider_id,
                    'to_address': "mox7n3wfu9hrT3Cn24RBTDce1wiHEP1NQp"
                    }

        response = client.post(reverse('transfer:send', kwargs={'selected_provider_id': provider_id}), post_data)
        response_html = self.stripHeaders(response)
        html_tree = self.validateHTML(response_html)
        print response_html
        # validate HTML
        self.assertNotEquals(html_tree, False)
        self.assertNotEquals(html_tree.xpath("//*[@id='passphrase']"), [])