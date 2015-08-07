"""
This module is used for translation of the QGEP project
"""
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QSettings, QLocale, QTranslator, QCoreApplication, pyqtSlot, QObject
import logging


def setupI18n(thePreferredLocale=None):
    """
    Setup internationalisation for the plugin.

    See if QGIS wants to override the system locale
    and then see if we can get a valid translation file
    for whatever locale is effectively being used.

    @param thePreferredLocale will override any other locale setting
    """

    logger = logging.getLogger(__name__)

    myOverrideFlag = QSettings().value('locale/overrideFlag', False, type=bool)

    myLocaleName = None
    if thePreferredLocale is not None:
        myLocaleName = thePreferredLocale
        logger.info('Using preferred locale: ' + myLocaleName)
    elif myOverrideFlag:
        myLocaleName = QSettings().value('locale/userLocale', u'')
        logger.info('Using QGIS override locale: ' + myLocaleName)
    else:
        myLocaleName = QLocale.system().name()
        # NOTES: we split the locale name because we need the first two
        # character i.e. 'id', 'af, etc
        myLocaleName = str(myLocaleName)
        logger.info('Using system default locale: ' + myLocaleName)

    # Insert into QT's translation system
    # As soon as translator gets deleted, the translation will stop
    # Therefore, QCoreApplication is set as parent to not delete it
    # while the application is running (but we might end up loading
    # the same translation twice)
    translator = QTranslator(QCoreApplication.instance())

    myTranslatorFile = 'qgepplugin_' + myLocaleName

    myResult = translator.load(myTranslatorFile, ':/plugins/qgepplugin/i18n')
    # myResult = translator.load( myTranslatorFile, '/home/kk/dev/python/QGEP/qgepplugin/i18n' )

    if myResult:
        QCoreApplication.instance().installTranslator(translator)

# pylint: disable=too-few-public-methods
class QgepJsTranslator(QObject):
    """
    Provides a callback method for the javascript code to support translation
    """

    def __init__(self):
        pass

    # pylint: disable=R0201
    @pyqtSlot(unicode, unicode, name='qsTr', result=unicode)
    def qsTr(self, context, sourceText):
        """
        Will be called by javascript code to perform translation of strings
        :param context:    The translation context
        :param sourceText: The string to translate
        :return:
        """
        return QApplication.translate(context, sourceText)
