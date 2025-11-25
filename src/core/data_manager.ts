
// ----------------------------------------------
// Record Item
// ----------------------------------------------
export enum eRecrodType {
    DEFAULT = "default",
    NOTE = "note"
}


interface iRecordItem {
    id:string;
    type: eRecrodType;
    [key: string]: any
}

class RecordItem implements iRecordItem {
    private _id:string = crypto.randomUUID();
    private _sourceData:Record<string,any> = {};

    constructor (sourceData?:Record<string,any>,public type:eRecrodType = eRecrodType.DEFAULT) {
        if (sourceData){
            this._sourceData = sourceData
            for (const key in sourceData) {
                if (!(key in this)) {
                    (this as any)[key] = sourceData[key]
                }
            }
        }
    }

    public get id () :string {
        return this._id
    }

    public get sourceData () :Record<string,any> {
        return this._sourceData
    }
}

// ----------------------------------------------
// Record Item
// ----------------------------------------------
enum eLinkType {
    DEFAULT = "Default"
}

interface iRecordLink {
    id:string;
    type: eLinkType;
    from: string;
    to: string;
}

class RecordLink implements iRecordLink {
    private _id:string;
    private _type:eLinkType;

    constructor (public from:string, public to:string, type?:eLinkType, id?:string) {
        this._id = id || crypto.randomUUID();
        this._type = type || eLinkType.DEFAULT
    }

    public get id () :string {
        return this._id
    }

    public get type () :eLinkType {
        return this._type
    }

    public set type (value:eLinkType) {
        this._type = value
    }
}

// ----------------------------------------------
// Listener & Callback
// ----------------------------------------------

export type DataRecord = RecordItem | RecordLink


export function is_DataRecord(obj: any): obj is DataRecord {
    return (
        typeof obj === 'object' &&
        obj !== null && 
        'id' in obj && 
        'type' in obj
    )
}
export enum eRecordCollections {
    ITEMRECORDS = "itemrecords",
    ITEMLINKS = "itemlinks"
}

function is_validRecordCollection(value: string): boolean {
  return Object.values(eRecordCollections).includes(value as eRecordCollections);
}

function get_RecordCollectionFromString (value: string): eRecordCollections | undefined {
  const enumValues = Object.values(eRecordCollections);
  if (enumValues.includes(value as eRecordCollections)) {
    return value as eRecordCollections;
  }
  return undefined;
}

type ListenerCallback = (records?: DataRecord[]) => void;;

interface RecordListener {
    target: eRecordCollections
    property?: string | null;
    callback: ListenerCallback;
}

// ----------------------------------------------
// Data Manager
// ----------------------------------------------

class DataManager {
    private static _instance: DataManager | null = null;

    private _recordItems: RecordItem[] = [];
    private _recordLinks: RecordLink[] = [];
    private _listeners: RecordListener[] = []
    private pendingNotifications: { [key: string]: boolean } = {};
    private notifyTimeout: number | undefined;
    private readonly timeoutMilisec:number = 50

    constructor () {
        this._recordItems = this.makeObservableArray<RecordItem>([], eRecordCollections.ITEMRECORDS);
        this._recordLinks = this.makeObservableArray<RecordLink>([], eRecordCollections.ITEMLINKS);
    }

    public static get Instance(): DataManager {
        if (!DataManager._instance) {
            DataManager._instance = new DataManager();
        }
        return DataManager._instance;
    }
    
    public get itemRecords() { return this._recordItems; }
    public set itemRecords(val: RecordItem[]) {
        this._recordItems = this.makeObservableArray(val, eRecordCollections.ITEMRECORDS);
        this.queueNotify(eRecordCollections.ITEMRECORDS);
    }

    public get itemLinks() { return this._recordLinks; }
    public set itemLinks(val: RecordLink[]) {
        this._recordLinks = this.makeObservableArray(val, eRecordCollections.ITEMLINKS);
        this.queueNotify(eRecordCollections.ITEMLINKS);
    }

    public addListener(collection: eRecordCollections, property: string | null, callback: ListenerCallback) {
        this._listeners.push({target:collection, property, callback});
    }

    private queueNotify(collection: eRecordCollections, property?: string) {
        const key = property ? `${collection}:${property}` : collection;
        this.pendingNotifications[key] = true;

        if (this.notifyTimeout !== undefined) {
            clearTimeout(this.notifyTimeout);
        }

        // Debounce to fire once after changes settle
        this.notifyTimeout = window.setTimeout(() => {
            this.flushNotifications();
        }, this.timeoutMilisec); // <-- Adjust debounce delay here
    }

    private makeObservableArray<T extends object>(arr: T[], collection: eRecordCollections): T[] {
        return new Proxy(arr, {
            set: (target, prop, value, receiver) => {
                const result = Reflect.set(target, prop, value, receiver);
                if (prop !== "length") {
                    this.queueNotify(collection, prop.toString());
                }
                return result;
            },
            deleteProperty(target, prop) {
                const result = Reflect.deleteProperty(target, prop);
                return result
            }
        });
    }

    private flushNotifications() {
        const keys = Object.keys(this.pendingNotifications);
        this.pendingNotifications = {};
        this.notifyTimeout = undefined;
        for (const { target, property, callback } of this._listeners) {
            const prefix = `${target.toLowerCase()}`
            const shouldNotify = keys.some(k => k === target || k.startsWith(prefix));
            if (shouldNotify) {
                const data = this.get_collection(target)
                callback(data||[])
            }
        }
    }

    public get_collection (collection:eRecordCollections) : DataRecord[]|null{
        switch (collection) {
            case eRecordCollections.ITEMRECORDS:
                return this.itemRecords
                break
            case eRecordCollections.ITEMLINKS :
                return this.itemLinks
                break
            default:
                return null
        }
    }

    public addRecord (sourceData:Record<string,any>, type?:eRecrodType) {
        const _record = new RecordItem(sourceData, type || eRecrodType.DEFAULT)
        this._recordItems.push(_record)
    }
}

export const DataMan = DataManager.Instance